local PythonVersion(pyversion='3.5') = {
  name: 'python' + std.strReplace(pyversion, '.', '') + '-pytest',
  image: 'python:' + pyversion,
  environment: {
    PY_COLORS: 1,
  },
  commands: [
    'pip install -r dev-requirements.txt -qq',
    'pip install -qq .',
    'ansible-doctor --help',
  ],
  depends_on: [
    'clone',
  ],
};

local PipelineLint = {
  kind: 'pipeline',
  name: 'lint',
  platform: {
    os: 'linux',
    arch: 'amd64',
  },
  steps: [
    {
      name: 'flake8',
      image: 'python:3.8',
      environment: {
        PY_COLORS: 1,
      },
      commands: [
        'pip install -r dev-requirements.txt -qq',
        'pip install -qq .',
        'flake8 ./ansibledoctor',
      ],
    },
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**', 'refs/pull/**'],
  },
};

local PipelineTest = {
  kind: 'pipeline',
  name: 'test',
  platform: {
    os: 'linux',
    arch: 'amd64',
  },
  steps: [
    PythonVersion(pyversion='3.5'),
    PythonVersion(pyversion='3.6'),
    PythonVersion(pyversion='3.7'),
    PythonVersion(pyversion='3.8'),
  ],
  depends_on: [
    'lint',
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**', 'refs/pull/**'],
  },
};

local PipelineSecurity = {
  kind: 'pipeline',
  name: 'security',
  platform: {
    os: 'linux',
    arch: 'amd64',
  },
  steps: [
    {
      name: 'bandit',
      image: 'python:3.8',
      environment: {
        PY_COLORS: 1,
      },
      commands: [
        'pip install -r dev-requirements.txt -qq',
        'pip install -qq .',
        'bandit -r ./ansibledoctor -x ./ansibledoctor/tests',
      ],
    },
  ],
  depends_on: [
    'test',
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**', 'refs/pull/**'],
  },
};

local PipelineBuildPackage = {
  kind: 'pipeline',
  name: 'build-package',
  platform: {
    os: 'linux',
    arch: 'amd64',
  },
  steps: [
    {
      name: 'build',
      image: 'python:3.8',
      commands: [
        'python setup.py sdist bdist_wheel',
      ],
    },
    {
      name: 'checksum',
      image: 'alpine',
      commands: [
        'cd dist/ && sha256sum * > ../sha256sum.txt',
      ],
    },
    {
      name: 'publish-github',
      image: 'plugins/github-release',
      settings: {
        overwrite: true,
        api_key: { from_secret: 'github_token' },
        files: ['dist/*', 'sha256sum.txt'],
        title: '${DRONE_TAG}',
        note: 'CHANGELOG.md',
      },
      when: {
        ref: ['refs/tags/**'],
      },
    },
    {
      name: 'publish-pypi',
      image: 'plugins/pypi',
      settings: {
        username: { from_secret: 'pypi_username' },
        password: { from_secret: 'pypi_password' },
        repository: 'https://upload.pypi.org/legacy/',
        skip_build: true,
      },
      when: {
        ref: ['refs/tags/**'],
      },
    },
  ],
  depends_on: [
    'security',
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**', 'refs/pull/**'],
  },
};

local PipelineBuildContainer(arch='amd64') = {
  kind: 'pipeline',
  name: 'build-container-' + arch,
  platform: {
    os: 'linux',
    arch: arch,
  },
  steps: [
    {
      name: 'build',
      image: 'python:3.8',
      commands: [
        'python setup.py bdist_wheel',
      ],
    },
    {
      name: 'dryrun',
      image: 'plugins/docker:18-linux-' + arch,
      settings: {
        dry_run: true,
        dockerfile: 'Dockerfile',
        repo: 'xoxys/ansible-doctor',
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
      },
      when: {
        ref: ['refs/pull/**'],
      },
    },
    {
      name: 'publish',
      image: 'plugins/docker:18-linux-' + arch,
      settings: {
        auto_tag: true,
        auto_tag_suffix: arch,
        dockerfile: 'Dockerfile',
        repo: 'xoxys/ansible-doctor',
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
      },
      when: {
        ref: ['refs/heads/master', 'refs/tags/**'],
      },
    },
  ],
  depends_on: [
    'security',
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**', 'refs/pull/**'],
  },
};

local PipelineDocs = {
  kind: 'pipeline',
  name: 'docs',
  platform: {
    os: 'linux',
    arch: 'amd64',
  },
  concurrency: {
    limit: 1,
  },
  steps: [
    {
      name: 'assets',
      image: 'byrnedo/alpine-curl',
      commands: [
        'mkdir -p docs/themes/hugo-geekdoc/',
        'curl -L https://github.com/xoxys/hugo-geekdoc/releases/latest/download/hugo-geekdoc.tar.gz | tar -xz -C docs/themes/hugo-geekdoc/ --strip-components=1',
      ],
    },
    {
      name: 'test',
      image: 'klakegg/hugo:0.59.1-ext-alpine',
      commands: [
        'cd docs/ && hugo-official',
      ],
    },
    {
      name: 'publish',
      image: 'plugins/s3-sync',
      settings: {
        access_key: { from_secret: 's3_access_key' },
        bucket: 'geekdocs',
        delete: true,
        endpoint: 'https://sp.rknet.org',
        path_style: true,
        secret_key: { from_secret: 's3_secret_access_key' },
        source: 'docs/public/',
        strip_prefix: 'docs/public/',
        target: '/${DRONE_REPO_NAME}',
      },
    },
  ],
  depends_on: [
    'build-package',
    'build-container-amd64',
    'build-container-arm64',
    'build-container-arm',
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**'],
  },
};

local PipelineNotifications = {
  kind: 'pipeline',
  name: 'notifications',
  platform: {
    os: 'linux',
    arch: 'amd64',
  },
  steps: [
    {
      image: 'plugins/manifest',
      name: 'manifest',
      settings: {
        ignore_missing: true,
        auto_tag: true,
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
        spec: 'manifest.tmpl',
      },
    },
    {
      name: 'readme',
      image: 'sheogorath/readme-to-dockerhub',
      environment: {
        DOCKERHUB_USERNAME: { from_secret: 'docker_username' },
        DOCKERHUB_PASSWORD: { from_secret: 'docker_password' },
        DOCKERHUB_REPO_PREFIX: 'xoxys',
        DOCKERHUB_REPO_NAME: 'ansible-doctor',
        README_PATH: 'README.md',
        SHORT_DESCRIPTION: 'ansible-doctor - Simple annotation based documentation for your roles',
      },
    },
    {
      name: 'matrix',
      image: 'plugins/matrix',
      settings: {
        homeserver: { from_secret: 'matrix_homeserver' },
        roomid: { from_secret: 'matrix_roomid' },
        template: 'Status: **{{ build.status }}**<br/> Build: [{{ repo.Owner }}/{{ repo.Name }}]({{ build.link }}) ({{ build.branch }}) by {{ build.author }}<br/> Message: {{ build.message }}',
        username: { from_secret: 'matrix_username' },
        password: { from_secret: 'matrix_password' },
      },
    },
  ],
  depends_on: [
    'docs',
  ],
  trigger: {
    ref: ['refs/heads/master', 'refs/tags/**'],
    status: ['success', 'failure'],
  },
};

[
  PipelineLint,
  PipelineTest,
  PipelineSecurity,
  PipelineBuildPackage,
  PipelineBuildContainer(arch='amd64'),
  PipelineBuildContainer(arch='arm64'),
  PipelineBuildContainer(arch='arm'),
  PipelineDocs,
  PipelineNotifications,
]
