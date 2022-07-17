local PythonVersion(pyversion='3.7') = {
  name: 'python' + std.strReplace(pyversion, '.', '') + '-pytest',
  image: 'python:' + pyversion,
  environment: {
    PY_COLORS: 1,
  },
  commands: [
    'pip install poetry poetry-dynamic-versioning -qq',
    'poetry config experimental.new-installer false',
    'poetry install',
    'poetry version',
    'poetry run ansible-doctor --help',
  ],
  depends_on: [
    'fetch',
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
      name: 'yapf',
      image: 'python:3.10',
      environment: {
        PY_COLORS: 1,
      },
      commands: [
        'git fetch -tq',
        'pip install poetry poetry-dynamic-versioning -qq',
        'poetry config experimental.new-installer false',
        'poetry install',
        'poetry run yapf -dr ./ansibledoctor',
      ],
    },
    {
      name: 'flake8',
      image: 'python:3.10',
      environment: {
        PY_COLORS: 1,
      },
      commands: [
        'git fetch -tq',
        'pip install poetry poetry-dynamic-versioning -qq',
        'poetry config experimental.new-installer false',
        'poetry install',
        'poetry run flake8 ./ansibledoctor',
      ],
    },
  ],
  trigger: {
    ref: ['refs/heads/main', 'refs/tags/**', 'refs/pull/**'],
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
    {
      name: 'fetch',
      image: 'python:3.10',
      commands: [
        'git fetch -tq',
      ],
    },
    PythonVersion(pyversion='3.7'),
    PythonVersion(pyversion='3.8'),
    PythonVersion(pyversion='3.9'),
    PythonVersion(pyversion='3.10'),
  ],
  depends_on: [
    'lint',
  ],
  trigger: {
    ref: ['refs/heads/main', 'refs/tags/**', 'refs/pull/**'],
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
      image: 'python:3.10',
      environment: {
        PY_COLORS: 1,
      },
      commands: [
        'git fetch -tq',
        'pip install poetry poetry-dynamic-versioning -qq',
        'poetry config experimental.new-installer false',
        'poetry install',
        'poetry run bandit -r ./ansibledoctor -x ./ansibledoctor/test',
      ],
    },
  ],
  depends_on: [
    'test',
  ],
  trigger: {
    ref: ['refs/heads/main', 'refs/tags/**', 'refs/pull/**'],
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
      image: 'python:3.10',
      commands: [
        'git fetch -tq',
        'pip install poetry poetry-dynamic-versioning -qq',
        'poetry build',
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
      name: 'changelog-generate',
      image: 'thegeeklab/git-chglog',
      commands: [
        'git fetch -tq',
        'git-chglog --no-color --no-emoji -o CHANGELOG.md ${DRONE_TAG:---next-tag unreleased unreleased}',
      ],
    },
    {
      name: 'changelog-format',
      image: 'thegeeklab/alpine-tools',
      commands: [
        'prettier CHANGELOG.md',
        'prettier -w CHANGELOG.md',
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
      image: 'python:3.10',
      commands: [
        'git fetch -tq',
        'pip install poetry poetry-dynamic-versioning -qq',
        'poetry publish -n',
      ],
      environment: {
        POETRY_HTTP_BASIC_PYPI_USERNAME: { from_secret: 'pypi_username' },
        POETRY_HTTP_BASIC_PYPI_PASSWORD: { from_secret: 'pypi_password' },
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
    ref: ['refs/heads/main', 'refs/tags/**', 'refs/pull/**'],
  },
};

local PipelineBuildContainer(arch='amd64') = {
  local build = if arch == 'arm' then [{
    name: 'build',
    image: 'python:3.10-alpine',
    commands: [
      'apk add -Uq --no-cache build-base openssl-dev libffi-dev musl-dev python3-dev git cargo',
      'git fetch -tq',
      'pip install poetry poetry-dynamic-versioning -qq',
      'poetry build',
    ],
    environment: {
      CARGO_NET_GIT_FETCH_WITH_CLI: true,
    },
  }] else [{
    name: 'build',
    image: 'python:3.10',
    commands: [
      'git fetch -tq',
      'pip install poetry poetry-dynamic-versioning -qq',
      'poetry build',
    ],
  }],

  kind: 'pipeline',
  name: 'build-container-' + arch,
  platform: {
    os: 'linux',
    arch: arch,
  },
  steps: build + [
    {
      name: 'dryrun',
      image: 'thegeeklab/drone-docker:19',
      settings: {
        dry_run: true,
        dockerfile: 'docker/Dockerfile.' + arch,
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
      image: 'thegeeklab/drone-docker:19',
      settings: {
        auto_tag: true,
        auto_tag_suffix: arch,
        dockerfile: 'docker/Dockerfile.' + arch,
        repo: 'thegeeklab/${DRONE_REPO_NAME}',
        username: { from_secret: 'docker_username' },
        password: { from_secret: 'docker_password' },
      },
      when: {
        ref: ['refs/heads/main', 'refs/tags/**'],
      },
      depends_on: ['dryrun'],
    },
    {
      name: 'publish-quay',
      image: 'thegeeklab/drone-docker:19',
      settings: {
        auto_tag: true,
        auto_tag_suffix: arch,
        dockerfile: 'docker/Dockerfile.' + arch,
        registry: 'quay.io',
        repo: 'quay.io/thegeeklab/${DRONE_REPO_NAME}',
        username: { from_secret: 'quay_username' },
        password: { from_secret: 'quay_password' },
      },
      when: {
        ref: ['refs/heads/main', 'refs/tags/**'],
      },
      depends_on: ['dryrun'],
    },
  ],
  depends_on: [
    'security',
  ],
  trigger: {
    ref: ['refs/heads/main', 'refs/tags/**', 'refs/pull/**'],
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
      image: 'thegeeklab/alpine-tools',
      commands: [
        'make doc',
      ],
    },
    {
      name: 'markdownlint',
      image: 'thegeeklab/markdownlint-cli',
      commands: [
        "markdownlint 'docs/content/**/*.md' 'README.md' 'CONTRIBUTING.md'",
      ],
    },
    {
      name: 'spellcheck',
      image: 'thegeeklab/alpine-tools',
      commands: [
        "spellchecker --files 'docs/content/**/*.md' 'README.md' -d .dictionary -p spell indefinite-article syntax-urls --no-suggestions",
      ],
      environment: {
        FORCE_COLOR: true,
        NPM_CONFIG_LOGLEVEL: 'error',
      },
    },
    {
      name: 'testbuild',
      image: 'thegeeklab/hugo:0.97.3',
      commands: [
        'hugo --panicOnWarning -s docs/ -b http://localhost:8000/',
      ],
    },
    {
      name: 'link-validation',
      image: 'thegeeklab/link-validator',
      commands: [
        'link-validator --nice --external --skip-file .linkcheckignore',
      ],
      environment: {
        LINK_VALIDATOR_BASE_DIR: 'docs/public',
      },
    },
    {
      name: 'build',
      image: 'thegeeklab/hugo:0.97.3',
      commands: [
        'hugo --panicOnWarning -s docs/',
      ],
    },
    {
      name: 'beautify',
      image: 'thegeeklab/alpine-tools',
      commands: [
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
      when: {
        ref: ['refs/heads/main', 'refs/tags/**'],
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
    ref: ['refs/heads/main', 'refs/tags/**', 'refs/pull/**'],
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
      image: 'thegeeklab/drone-matrix',
      settings: {
        homeserver: { from_secret: 'matrix_homeserver' },
        roomid: { from_secret: 'matrix_roomid' },
        template: 'Status: **{{ build.Status }}**<br/> Build: [{{ repo.Owner }}/{{ repo.Name }}]({{ build.Link }}){{#if build.Branch}} ({{ build.Branch }}){{/if}} by {{ commit.Author }}<br/> Message: {{ commit.Message.Title }}',
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
    ref: ['refs/heads/main', 'refs/tags/**'],
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
