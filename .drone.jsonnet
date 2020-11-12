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
      image: 'python:3.9',
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
    PythonVersion(pyversion='3.9'),
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
      image: 'python:3.9',
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
      image: 'python:3.9',
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
      image: 'python:3.9',
      commands: [
        'python setup.py bdist_wheel',
      ],
    },
    {
      name: 'dryrun',
      image: 'plugins/docker:18-linux-' + arch,
      settings: {
        dry_run: true,
        dockerfile: 'docker/Dockerfile',
        repo: 'thegeeklab/${DRONE_REPO_NAME}',
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
      },
      depends_on: ['build'],
      when: {
        ref: ['refs/pull/**'],
      },
    },
    {
      name: 'publish-dockerhub',
      image: 'plugins/docker:18-linux-' + arch,
      settings: {
        auto_tag: true,
        auto_tag_suffix: arch,
        dockerfile: 'docker/Dockerfile',
        repo: 'thegeeklab/${DRONE_REPO_NAME}',
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
      },
      when: {
        ref: ['refs/heads/master', 'refs/tags/**'],
      },
      depends_on: ['dryrun'],
    },
    {
      name: 'publish-quay',
      image: 'plugins/docker:18-linux-' + arch,
      settings: {
        auto_tag: true,
        auto_tag_suffix: arch,
        dockerfile: 'docker/Dockerfile',
        registry: 'quay.io',
        repo: 'quay.io/thegeeklab/${DRONE_REPO_NAME}',
        username: { from_secret: 'quay_username' },
        password: { from_secret: 'quay_password' },
      },
      when: {
        ref: ['refs/heads/master', 'refs/tags/**'],
      },
      depends_on: ['dryrun'],
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
      name: 'generate',
      image: 'thegeeklab/alpine-tools',
      commands: [
        'make doc',
      ],
    },
    {
      name: 'markdownlint',
      image: 'node:lts-alpine',
      commands: [
        'npm install -g markdownlint-cli',
        "markdownlint 'docs/content/**/*.md' 'README.md'",
      ],
      environment: {
        FORCE_COLOR: true,
        NPM_CONFIG_LOGLEVEL: 'error',
      },
    },
    {
      name: 'spellcheck',
      image: 'node:lts-alpine',
      commands: [
        'npm install -g spellchecker-cli',
        "spellchecker --files 'docs/content/**/*.md' 'README.md' -d .dictionary -p spell indefinite-article syntax-urls --no-suggestions",
      ],
      environment: {
        FORCE_COLOR: true,
        NPM_CONFIG_LOGLEVEL: 'error',
      },
    },
    {
      name: 'testbuild',
      image: 'klakegg/hugo:0.74.3-ext-alpine',
      commands: [
        'hugo-official -s docs/ -b http://localhost/',
      ],
    },
    {
      name: 'link-validation',
      image: 'thegeeklab/link-validator',
      commands: [
        'link-validator -ro',
      ],
      environment: {
        LINK_VALIDATOR_BASE_DIR: 'docs/public',
      },
    },
    {
      name: 'build',
      image: 'klakegg/hugo:0.74.3-ext-alpine',
      commands: [
        'hugo-official -s docs/',
      ],
    },
    {
      name: 'beautify',
      image: 'node:lts-alpine',
      commands: [
        'npm install -g js-beautify',
        "html-beautify -r -f 'docs/public/**/*.html'",
      ],
      environment: {
        FORCE_COLOR: true,
        NPM_CONFIG_LOGLEVEL: 'error',
      },
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
      name: 'manifest-dockerhub',
      settings: {
        ignore_missing: true,
        auto_tag: true,
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
        spec: 'docker/manifest.tmpl',
      },
      when: {
        status: ['success'],
      },
    },
    {
      image: 'plugins/manifest',
      name: 'manifest-quay',
      settings: {
        ignore_missing: true,
        auto_tag: true,
        username: { from_secret: 'quay_username' },
        password: { from_secret: 'quay_password' },
        spec: 'docker/manifest-quay.tmpl',
      },
      when: {
        status: ['success'],
      },
    },
    {
      name: 'pushrm-dockerhub',
      pull: 'always',
      image: 'chko/docker-pushrm:1',
      environment: {
        DOCKER_PASS: {
          from_secret: 'docker_password',
        },
        DOCKER_USER: {
          from_secret: 'docker_username',
        },
        PUSHRM_FILE: 'README.md',
        PUSHRM_SHORT: 'Annotation based documentation for your Ansible roles',
        PUSHRM_TARGET: 'thegeeklab/${DRONE_REPO_NAME}',
      },
      when: {
        status: ['success'],
      },
    },
    {
      name: 'pushrm-quay',
      pull: 'always',
      image: 'chko/docker-pushrm:1',
      environment: {
        APIKEY__QUAY_IO: {
          from_secret: 'quay_token',
        },
        PUSHRM_FILE: 'README.md',
        PUSHRM_TARGET: 'quay.io/thegeeklab/${DRONE_REPO_NAME}',
      },
      when: {
        status: ['success'],
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
      when: {
        status: ['success', 'failure'],
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
