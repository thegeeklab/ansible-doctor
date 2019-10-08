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

local PipelineBuild = {
    kind: "pipeline",
    name: "build",
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
            name: "publish-gitea",
            image: "plugins/gitea-release",
            pull: "always",
            settings: {
                base_url: "https://gitea.owncloud.services",
                api_key: { "from_secret": "gitea_token"},
                files: ["dist/*", "sha256sum.txt"],
                title: "${DRONE_TAG}",
                note: "CHANGELOG.md",
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

[
    PipelineLint,
    PipelineTest,
    PipelineSecurity,
    PipelineBuild,
]
