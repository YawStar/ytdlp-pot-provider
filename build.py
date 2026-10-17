import os
import shutil
import subprocess
import sys
import zipfile

# Build လုပ်မည့် Target ဇယား (32-bit နှင့် 64-bit အစုံအလင်)
targets = [
    # 64-bit Targets
    {"os": "windows", "arch": "amd64", "ext": ".exe"},  # Windows 64-bit
    {"os": "windows", "arch": "arm64", "ext": ".exe"},  # Windows ARM64
    {"os": "linux", "arch": "amd64", "ext": ""},        # Linux 64-bit
    {"os": "linux", "arch": "arm64", "ext": ""},        # Linux / Android Termux ARM64
    {"os": "darwin", "arch": "amd64", "ext": ""},       # Intel Mac
    {"os": "darwin", "arch": "arm64", "ext": ""},       # Apple Silicon Mac
    
    # 32-bit Targets
    {"os": "windows", "arch": "386", "ext": ".exe"},    # Windows 32-bit (x86)
    {"os": "linux", "arch": "386", "ext": ""},          # Linux 32-bit (x86)
    {"os": "linux", "arch": "arm", "ext": ""},          # Linux ARM 32-bit (Raspberry Pi)
]


def zip_yt_dlp_plugins(dist_dir: str):
    plugins_dir = "yt_dlp_plugins"

    if not os.path.isdir(plugins_dir):
        print(
            f"Warning: '{plugins_dir}' directory not found, skipping zip archive creation.",
            file=sys.stderr,
        )
        return

    zip_filename = os.path.join(dist_dir, "yawstar-ytdlp-pot-provider.zip")
    print(f"\nPackaging '{plugins_dir}' into '{zip_filename}'...")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(plugins_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # zip ထဲမှာ yt_dlp_plugins/... structure အတိုင်း ရောက်ရှိစေရန် arcname သတ်မှတ်ခြင်း
                arcname = os.path.relpath(file_path, start=".")
                zipf.write(file_path, arcname)

    print(f"Plugin package created successfully: {zip_filename}")


def build():
    dist_dir = "dist"
    os.makedirs(dist_dir, exist_ok=True)

    # Go တွေရှိတဲ့ ဖိုဒါ
    server_dir = "server"

    if not os.path.isdir(server_dir):
        print(f"Error: '{server_dir}' directory not found!", file=sys.stderr)
        sys.exit(1)

    for target in targets:
        go_os = target["os"]
        go_arch = target["arch"]
        ext = target["ext"]

        output_name = f"yawstar-pot-server-{go_os}-{go_arch}{ext}"
        output_path = os.path.abspath(os.path.join(dist_dir, output_name))

        print(f"Building for {go_os}/{go_arch}...")

        env = os.environ.copy()
        env["GOOS"] = go_os
        env["GOARCH"] = go_arch

        # module path ပြဿနာ မဖြစ်အောင် server ဖိုဒါထဲကို ဝင်ပြီး build လုပ်
        cmd = ["go", "build", "-o", output_path, "."]
        result = subprocess.run(cmd, cwd=server_dir, env=env)

        if result.returncode != 0:
            print(f"Error building for {go_os}/{go_arch}", file=sys.stderr)
            sys.exit(1)

    print(
        f"\nBuild complete! All binaries are saved in the '{dist_dir}' folder."
    )

    # yt_dlp_plugins ဖိုဒါကို zip Archive အဖြစ် ထုပ်ပိုးခြင်း
    zip_yt_dlp_plugins(dist_dir)


if __name__ == "__main__":
    build()