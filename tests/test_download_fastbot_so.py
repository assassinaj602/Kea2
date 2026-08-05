import importlib.util
from pathlib import Path

PROJECT_ROOT = Path(__file__).parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


fastbot_so_downloader = load_module(
    "fastbot_so_downloader",
    PROJECT_ROOT / "kea2" / "fastbot_so_downloader.py",
)
kea_launcher = load_module("kea_launcher", PROJECT_ROOT / "kea2" / "kea_launcher.py")
download_fastbot_so = load_module("download_fastbot_so", PROJECT_ROOT / "scripts" / "download_fastbot_so.py")


def test_library_urls_include_github_and_gitee_for_the_requested_version():
    sources = dict(fastbot_so_downloader.raw_library_urls("v1.2.3", "arm64-v8a"))

    assert sources["GitHub"].startswith("https://raw.githubusercontent.com/ecnusse/Kea2/v1.2.3/")
    assert sources["GitHub"].endswith("/kea2/assets/fastbot_libs/arm64-v8a/libfastbot_native.so")
    assert sources["Gitee"].startswith("https://gitee.com/XixianLiang/Kea2/raw/v1.2.3/")


def test_missing_abis_reuses_valid_cached_libraries(tmp_path):
    for abi in fastbot_so_downloader.ABIS:
        path = fastbot_so_downloader.library_path(tmp_path, "v1.2.3", abi)
        path.parent.mkdir(parents=True)
        path.write_bytes(b"\x7fELFtest")

    assert list(fastbot_so_downloader.missing_abis(tmp_path, "v1.2.3", force=False)) == []
    assert list(fastbot_so_downloader.missing_abis(tmp_path, "v1.2.3", force=True)) == list(fastbot_so_downloader.ABIS)


def test_parse_args_accepts_an_unlisted_version_and_rejects_invalid_refs():
    args = download_fastbot_so.parse_args(["--version", "v9.9.9"])
    assert args.version == "v9.9.9"

    try:
        download_fastbot_so.parse_args(["--version", "../../unexpected"])
    except SystemExit as error:
        assert error.code == 2
    else:
        raise AssertionError("unsupported versions must be rejected")


def test_main_uses_gitee_when_github_download_fails(tmp_path, monkeypatch):
    attempted_urls = []

    def fake_download(url, destination, timeout):
        attempted_urls.append(url)
        if "raw.githubusercontent.com" in url:
            raise fastbot_so_downloader.URLError("GitHub unavailable")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(b"\x7fELFtest")

    monkeypatch.setattr(fastbot_so_downloader, "download_file", fake_download)
    monkeypatch.setattr(fastbot_so_downloader, "is_valid_library", lambda path: path.exists())

    assert fastbot_so_downloader.ensure_libraries("v1.2.3", cache_dir=tmp_path) == tmp_path / "v1.2.3"
    assert len(attempted_urls) == len(fastbot_so_downloader.ABIS) * 2
    assert all("gitee.com" in url for url in attempted_urls[1::2])


def test_kea_cli_accepts_fastbot_so_version():
    args = kea_launcher.parse_args(["run", "-p", "com.example.app", "--fastbot-so-version", "v1.2.3"])

    assert args.fastbot_so_version == "v1.2.3"
