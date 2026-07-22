import subprocess

from scripts import verify


class FakeProcess:
    def __init__(self, *, returncode=0, timeout_once=False):
        self.pid = 43210
        self.returncode = returncode
        self.timeout_once = timeout_once
        self.wait_calls = []
        self.killed = False

    def poll(self):
        return None if self.timeout_once else self.returncode

    def wait(self, timeout=None):
        self.wait_calls.append(timeout)
        if self.timeout_once:
            self.timeout_once = False
            raise subprocess.TimeoutExpired(["python", "-m", "pytest"], timeout)
        return self.returncode

    def kill(self):
        self.killed = True


def test_run_returns_child_exit_code_without_cleanup(monkeypatch):
    process = FakeProcess(returncode=7)
    cleanup_calls = []
    monkeypatch.setattr(verify.subprocess, "Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr(
        verify, "_terminate_process_tree", lambda child: cleanup_calls.append(child)
    )

    code = verify.run(["python", "-m", "pytest"], {}, timeout=30)

    assert code == 7
    assert cleanup_calls == []


def test_run_timeout_cleans_only_spawned_process_tree(monkeypatch):
    process = FakeProcess(timeout_once=True)
    cleanup_calls = []
    monkeypatch.setattr(verify.subprocess, "Popen", lambda *args, **kwargs: process)
    monkeypatch.setattr(
        verify, "_terminate_process_tree", lambda child: cleanup_calls.append(child)
    )

    code = verify.run(["python", "-m", "pytest"], {}, timeout=30)

    assert code == 124
    assert cleanup_calls == [process]


def test_windows_cleanup_targets_spawned_pid_tree(monkeypatch):
    process = FakeProcess(timeout_once=True)
    commands = []

    def record_run(command, **kwargs):
        commands.append((command, kwargs))
        process.timeout_once = False

    monkeypatch.setattr(verify.subprocess, "run", record_run)

    verify._terminate_process_tree(
        process, platform_name="nt", grace_seconds=1
    )

    assert commands[0][0] == ["taskkill", "/PID", "43210", "/T", "/F"]
    assert process.killed is False


def test_full_profile_runs_one_complete_pytest_command(monkeypatch, tmp_path):
    commands = []
    monkeypatch.setattr(verify.tempfile, "gettempdir", lambda: str(tmp_path))
    monkeypatch.setattr(
        verify,
        "run",
        lambda command, env, timeout: commands.append((command, env, timeout)) or 0,
    )

    assert verify.main(["--profile", "full"]) == 0

    pytest_commands = [
        command
        for command, _env, _timeout in commands
        if command[1:4] == ["-m", "pytest", "-q"]
    ]
    assert pytest_commands == [[verify.sys.executable, "-m", "pytest", "-q", "tests"]]
    assert all(env["NIKO_ACCEPTANCE_LIVE"] == "0" for _command, env, _timeout in commands)
