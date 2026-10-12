import os
import subprocess
import sys

# Build လုပ်မည့် Target ဇယား
targets = [
    {"os": "windows", "arch": "amd64", "ext": ".exe"},
    {"os": "linux", "arch": "amd64", "ext": ""},
    {"os": "darwin", "arch": "amd64", "ext": ""},      # Intel Mac
    {"os": "darwin", "arch": "arm64", "ext": ""},      # Apple Silicon Mac (M1/M2/M3)
]

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
            
    print(f"\nBuild complete! All binaries are saved in the '{dist_dir}' folder.")

if __name__ == "__main__":
    build()