local PythonVersion(pyversion="3.5") = {
    name: "python" + std.strReplace(pyversion, '.', '') + "-pytest",
    image: "python:" + pyversion,
    pull: "always",
    environment: {
        PY_COLORS: 1
    },
    commands: [
        "pip install -r test-requirements.txt -qq",
        "pip install -qq .",
        "ansible-doctor --help",
    ],
    depends_on: [
        "clone",
    ],
};

local PipelineLint = {
    kind: "pipeline",
    name: "lint",
    platform: {
        os: "linux",
        arch: "amd64",
    },
    steps: [
        {
            name: "flake8",
            image: "python:3.7",
            pull: "always",
            environment: {
                PY_COLORS: 1
            },
            commands: [
                "pip install -r test-requirements.txt -qq",
                "pip install -qq .",
                "flake8 ./ansibledoctor",
            ],
        },
    ],
    trigger: {
        ref: ["refs/heads/master", "refs/tags/**", "refs/pull/**"],
    },
};

local PipelineTest = {
    kind: "pipeline",
    name: "test",
    platform: {
        os: "linux",
        arch: "amd64",
    },
    steps: [
        PythonVersion(pyversion="3.5"),
        PythonVersion(pyversion="3.6"),
        PythonVersion(pyversion="3.7"),
        PythonVersion(pyversion="3.8-rc"),
    ],
    trigger: {
        ref: ["refs/heads/master", "refs/tags/**", "refs/pull/**"],
    },
    depends_on: [
        "lint",
    ],
};

local PipelineSecurity = {
    kind: "pipeline",
    name: "security",
    platform: {
        os: "linux",
        arch: "amd64",
    },
    steps: [
        {
            name: "bandit",
            image: "python:3.7",
            pull: "always",
            environment: {
                PY_COLORS: 1
            },
            commands: [
                "pip install -r test-requirements.txt -qq",
                "pip install -qq .",
                "bandit -r ./ansibledoctor -x ./ansibledoctor/tests",
            ],
        },
    ],
    depends_on: [
        "test",
    ],
    trigger: {
        ref: ["refs/heads/master", "refs/tags/**", "refs/pull/**"],
    },
};

local PipelineBuildPackage = {
    kind: "pipeline",
    name: "build-package",
    platform: {
        os: "linux",
        arch: "amd64",
    },
    steps: [
        {
            name: "build",
            image: "python:3.7",
            pull: "always",
            commands: [
                "python setup.py sdist bdist_wheel",
            ]
        },
        {
            name: "checksum",
            image: "alpine",
            pull: "always",
            commands: [
                "cd dist/ && sha256sum * > sha256sum.txt"
            ],
        },
        {
            name: "publish-github",
            image: "plugins/github-release",
            pull: "always",
            settings: {
                overwrite: true,
                api_key: { "from_secret": "github_token"},
                files: ["dist/*", "sha256sum.txt"],
                title: "${DRONE_TAG}",
                note: "CHANGELOG.md",
            },
            when: {
                ref: [ "refs/tags/**" ],
            },
        },
        {
          name: "publish-pypi",
          image: "plugins/pypi",
          pull: "always",
          settings: {
            username: { "from_secret": "pypi_username" },
            password: { "from_secret": "pypi_password" },
            repository: "https://upload.pypi.org/legacy/",
            skip_build: true
          },
          when: {
            ref: [ "refs/tags/**" ],
          },
        },
    ],
    depends_on: [
        "security",
    ],
    trigger: {
        ref: ["refs/heads/master", "refs/tags/**", "refs/pull/**"],
    },
};

local PipelineBuildContainer(arch="amd64") = {
  kind: "pipeline",
  name: "build-container-" + arch,
  platform: {
    os: "linux",
    arch: arch,
  },
  steps: [
    {
      name: "build",
      image: "python:3.7",
      pull: "always",
      commands: [
          "python setup.py bdist_wheel",
      ]
    },
    {
      name: "dryrun",
      image: "plugins/docker:linux-" + arch,
      pull: "always",
      settings: {
        dry_run: true,
        tags: arch,
        dockerfile: "Dockerfile",
        repo: "xoxys/ansible-doctor",
        username: { "from_secret": "docker_username" },
        password: { "from_secret": "docker_password" },
      }
    },
    {
      name: "publish",
      image: "plugins/docker:linux-" + arch,
      pull: "always",
      settings: {
        auto_tag: true,
        auto_tag_suffix: arch,
        dockerfile: "Dockerfile",
        repo: "xoxys/ansible-doctor",
        username: { "from_secret": "docker_username" },
        password: { "from_secret": "docker_password" },
      },
      when: {
          ref: [ "refs/tags/**" ],
      },
    },
  ],
  depends_on: [
    "security",
  ],
  trigger: {
      ref: ["refs/heads/master", "refs/tags/**", "refs/pull/**"],
  },
};

local PipelineNotifications = {
  kind: "pipeline",
  name: "notifications",
  platform: {
    os: "linux",
    arch: "amd64",
  },
  steps: [
    {
      name: "matrix",
      image: "plugins/matrix",
      settings: {
        template: "Status: **{{ build.status }}**<br/> Build: [{{ repo.Owner }}/{{ repo.Name }}]({{ build.link }}) ({{ build.branch }}) by {{ build.author }}<br/> Message: {{ build.message }}",
        roomid: { "from_secret": "matrix_roomid" },
        homeserver: { "from_secret": "matrix_homeserver" },
        username: { "from_secret": "matrix_username" },
        password: { "from_secret": "matrix_password" },
      },
    },
  ],
  depends_on: [
    "build-package",
    "build-container-amd64",
    "build-container-arm64",
    "build-container-arm"
  ],
  trigger: {
    ref: ["refs/heads/master", "refs/tags/**"],
    status: [ "success", "failure" ],
  },
};

[
    PipelineLint,
    PipelineTest,
    PipelineSecurity,
    PipelineBuildPackage,
    PipelineBuildContainer(arch="amd64"),
    PipelineBuildContainer(arch="arm64"),
    PipelineBuildContainer(arch="arm"),
    PipelineNotifications,
]
