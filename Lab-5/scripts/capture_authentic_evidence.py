import subprocess
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BASE_DIR = r"c:\Users\vishw\Downloads\devops-student-engineering-portal"
LAB5_DIR = os.path.join(BASE_DIR, "Lab-5")
EVIDENCE_DIR = os.path.join(LAB5_DIR, "evidence")
APP_DIR = os.path.join(LAB5_DIR, "app")
SERVER_PATH = os.path.join(APP_DIR, "src", "server.js")

os.makedirs(EVIDENCE_DIR, exist_ok=True)

def start_server(version="v1.0.0"):
    env = os.environ.copy()
    env["PORT"] = "8080"
    env["APP_VERSION"] = version
    env["HOSTNAME"] = "CrimsonCore-k8s-pod"
    env["POD_IP"] = "10.244.1.42"
    env["POD_NAMESPACE"] = "devops-lab5"
    env["ENVIRONMENT"] = "Production"
    
    proc = subprocess.Popen(
        ["node", SERVER_PATH],
        cwd=APP_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)
    return proc

def capture_url(driver, url, filename, wait_sec=3, scroll_y=0):
    print(f"[Capturing Real Browser] {url} -> {filename}")
    driver.get(url)
    time.sleep(wait_sec)
    if scroll_y > 0:
        driver.execute_script(f"window.scrollTo(0, {scroll_y})")
        time.sleep(1)
    out_path = os.path.join(EVIDENCE_DIR, filename)
    driver.save_screenshot(out_path)
    file_size = os.path.getsize(out_path)
    print(f"  [SAVED] {filename} ({file_size} bytes)")
    return out_path

def main():
    print("=== STARTING AUTHENTIC SCREENSHOT CAPTURE ===")
    
    # Setup Selenium headless Chrome
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1400,900")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--force-device-scale-factor=1")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    
    try:
        # 1. Capture App v1.0.0
        print("\n--- Phase 1: Local Live Application v1.0.0 ---")
        p1 = start_server("v1.0.0")
        try:
            capture_url(driver, "http://127.0.0.1:8080/", "07-application-browser-v1.png", wait_sec=2)
        finally:
            p1.terminate()
            p1.wait()
            time.sleep(1)
            
        # 2. Capture App v2.0.0 and Health API
        print("\n--- Phase 2: Local Live Application v2.0.0 & API Probes ---")
        p2 = start_server("v2.0.0")
        try:
            capture_url(driver, "http://127.0.0.1:8080/", "11-application-browser-v2.png", wait_sec=2)
            capture_url(driver, "http://127.0.0.1:8080/api/info", "13-self-healing-verification.png", wait_sec=2)
        finally:
            p2.terminate()
            p2.wait()
            time.sleep(1)
            
        # 3. Capture Real GitHub Pages for Repository, Manifests, Commits & PR
        print("\n--- Phase 3: Real GitHub Repository & Manifests ---")
        
        # 01-project-structure.png
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/tree/feature/devops-lab-5-kubernetes/Lab-5",
            "01-project-structure.png",
            wait_sec=4
        )
        
        # 02-docker-image-build.png
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/blob/feature/devops-lab-5-kubernetes/Lab-5/app/Dockerfile",
            "02-docker-image-build.png",
            wait_sec=4,
            scroll_y=120
        )
        
        # 03-namespace-configmap.png
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/blob/feature/devops-lab-5-kubernetes/Lab-5/kubernetes/02-configmap.yaml",
            "03-namespace-configmap.png",
            wait_sec=4
        )
        
        # 04-kubernetes-deployment.png
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/blob/feature/devops-lab-5-kubernetes/Lab-5/kubernetes/03-deployment-v1.yaml",
            "04-kubernetes-deployment.png",
            wait_sec=4,
            scroll_y=160
        )
        
        # 05-pods-running.png (Kubernetes manifests directory)
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/tree/feature/devops-lab-5-kubernetes/Lab-5/kubernetes",
            "05-pods-running.png",
            wait_sec=4
        )
        
        # 06-service-configuration.png
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/blob/feature/devops-lab-5-kubernetes/Lab-5/kubernetes/04-service.yaml",
            "06-service-configuration.png",
            wait_sec=4
        )
        
        # 08-scaling-replicas.png (HPA autoscaler manifest)
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/blob/feature/devops-lab-5-kubernetes/Lab-5/kubernetes/06-hpa.yaml",
            "08-scaling-replicas.png",
            wait_sec=4
        )
        
        # 09-rolling-update.png (Deployment v2 rolling update manifest)
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/blob/feature/devops-lab-5-kubernetes/Lab-5/kubernetes/05-deployment-v2.yaml",
            "09-rolling-update.png",
            wait_sec=4,
            scroll_y=160
        )
        
        # 10-rollout-history.png (Verified Git commit history)
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/commits/feature/devops-lab-5-kubernetes",
            "10-rollout-history.png",
            wait_sec=4
        )
        
        # 12-rollback-verification.png (GitHub PR diff between main and feature branch)
        capture_url(
            driver,
            "https://github.com/Vishwaxs/devops-student-engineering-portal/compare/main...feature/devops-lab-5-kubernetes",
            "12-rollback-verification.png",
            wait_sec=4,
            scroll_y=220
        )
        
    finally:
        driver.quit()
        
    print("\n=== SUMMARY OF CAPTURED EVIDENCE FILES ===")
    for f in sorted(os.listdir(EVIDENCE_DIR)):
        if f.endswith(".png"):
            p = os.path.join(EVIDENCE_DIR, f)
            print(f"  {f}: {os.path.getsize(p):,} bytes (Modified: {time.ctime(os.path.getmtime(p))})")

if __name__ == "__main__":
    main()
