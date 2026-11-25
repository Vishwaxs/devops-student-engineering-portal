import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = r"c:\Users\vishw\Downloads\devops-student-engineering-portal\Lab-6"
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence")
PDF_PATH = os.path.join(BASE_DIR, "Lab6_DevOps_Kubernetes_Report.pdf")


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(50, 11 * 72 - 34, "CHRIST (Deemed to be University) · Dept of Computer Science · MCA DevOps Lab 6")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(50, 11 * 72 - 40, 8.5 * 72 - 50, 11 * 72 - 40)
        self.line(50, 44, 8.5 * 72 - 50, 44)
        self.drawString(50, 31, "Lab Exercise 6: Jobs, CronJobs, ConfigMaps, Secrets & Helm")
        self.drawRightString(8.5 * 72 - 50, 31, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def make_figure(filename, caption, observation, body_style, cap_style, obs_style, target_width=430):
    img_path = os.path.join(EVIDENCE_DIR, filename)
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing evidence file: {img_path}")
    with PILImage.open(img_path) as im:
        w, h = im.size
    scaled_h = target_width * (h / float(w))
    block = [
        Image(img_path, width=target_width, height=scaled_h),
        Spacer(1, 3),
        Paragraph(f"<i>{caption}</i>", cap_style),
    ]
    if observation:
        block.append(Spacer(1, 5))
        block.append(Paragraph(f"<b>Observation:</b> {observation}", obs_style))
    block.append(Spacer(1, 8))
    return KeepTogether(block)


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=52,
        bottomMargin=52,
    )

    styles = getSampleStyleSheet()
    c_primary = colors.HexColor("#1e3a8a")
    c_secondary = colors.HexColor("#0284c7")
    c_accent = colors.HexColor("#059669")

    title_style = ParagraphStyle(
        "CoverTitle", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=22, leading=28, textColor=c_primary, alignment=1, spaceAfter=10,
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"], fontName="Helvetica",
        fontSize=12, leading=16, textColor=colors.HexColor("#475569"), alignment=1, spaceAfter=24,
    )
    h1_style = ParagraphStyle(
        "H1", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=13.5, leading=18, textColor=c_primary, spaceBefore=10, spaceAfter=5, keepWithNext=True,
    )
    h2_style = ParagraphStyle(
        "H2", parent=styles["Normal"], fontName="Helvetica-Bold",
        fontSize=10.5, leading=14, textColor=c_secondary, spaceBefore=7, spaceAfter=4, keepWithNext=True,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"], fontName="Helvetica",
        fontSize=9, leading=13, textColor=colors.HexColor("#1e293b"), spaceAfter=5,
    )
    bullet_style = ParagraphStyle(
        "Bullet", parent=body_style, leftIndent=14, firstLineIndent=-9, spaceAfter=3,
    )
    code_style = ParagraphStyle(
        "Code", parent=styles["Normal"], fontName="Courier", fontSize=7.8, leading=10.5,
        textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.5, borderPadding=5,
        spaceAfter=6, spaceBefore=3,
    )
    cap_style = ParagraphStyle(
        "Cap", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=8,
        leading=10.5, alignment=1, textColor=colors.HexColor("#475569"), spaceAfter=2,
    )
    obs_style = ParagraphStyle(
        "Obs", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5,
        leading=12, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"), borderWidth=0.4, borderPadding=4,
    )

    story = []

    # =========================================================================
    # 1. COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 36))
    story.append(Paragraph("CHRIST (DEEMED TO BE UNIVERSITY)", ParagraphStyle("Uni", fontName="Helvetica-Bold", fontSize=15, leading=18, alignment=1, textColor=c_primary)))
    story.append(Paragraph("SCHOOL OF SCIENCES · DEPARTMENT OF COMPUTER SCIENCE", ParagraphStyle("Dept", fontName="Helvetica", fontSize=9.5, leading=13, alignment=1, textColor=colors.HexColor("#64748b"))))
    story.append(Paragraph("BANGALORE CENTRAL CAMPUS, KARNATAKA, INDIA", ParagraphStyle("Loc", fontName="Helvetica", fontSize=8.5, leading=12, alignment=1, textColor=colors.HexColor("#94a3b8"))))
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width="80%", thickness=2, color=c_secondary, spaceAfter=26))
    story.append(Paragraph("MCA DEVOPS LAB EXERCISE — 6", ParagraphStyle("LabTag", fontName="Helvetica-Bold", fontSize=11, leading=14, alignment=1, textColor=c_accent)))
    story.append(Paragraph("KUBERNETES JOBS, CRONJOBS, CONFIGMAPS, SECRETS AND HELM", title_style))
    story.append(Paragraph("Practical Implementation, Execution Logs, Application Verification and Release Management Report", subtitle_style))
    story.append(HRFlowable(width="40%", thickness=0.8, color=colors.HexColor("#cbd5e1"), spaceAfter=28))

    meta_data = [
        [Paragraph("<b>Course:</b>", body_style), Paragraph("2026-5 MCA B-DevOps (Master of Computer Applications)", body_style)],
        [Paragraph("<b>Student Name:</b>", body_style), Paragraph("Vishwas Vashishtha", body_style)],
        [Paragraph("<b>Email:</b>", body_style), Paragraph("vishwas.vashishtha@mca.christuniversity.in", body_style)],
        [Paragraph("<b>Faculty In-Charge:</b>", body_style), Paragraph("Cynthia T, Department of Computer Science", body_style)],
        [Paragraph("<b>Max Marks:</b>", body_style), Paragraph("100 Points", body_style)],
        [Paragraph("<b>Submission Date:</b>", body_style), Paragraph("November 26, 2026", body_style)],
        [Paragraph("<b>Execution Cluster:</b>", body_style), Paragraph("Killercoda Kubernetes v1.37.1 (2 Nodes: controlplane, node01) &amp; Helm v4.3.0", body_style)],
        [Paragraph("<b>Repository &amp; Branch:</b>", body_style), Paragraph("github.com/Vishwaxs/devops-student-engineering-portal (<code>feature/devops-lab-6-jobs-cronjobs-helm</code>)", body_style)],
    ]
    t_meta = Table(meta_data, colWidths=[130, 345])
    t_meta.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 24))
    story.append(Paragraph("<i>Note: All outputs and screenshots in this report were captured directly from the active Killercoda Kubernetes cluster and Chrome browser during execution. No secret values are exposed.</i>", cap_style))
    story.append(PageBreak())

    # =========================================================================
    # 2. AIM AND OBJECTIVES & 3. PROJECT ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("1. Aim and Objectives", h1_style))
    story.append(Paragraph("<b>Aim:</b> To create and execute Kubernetes Jobs and CronJobs, separate non-sensitive configuration and dummy credentials using ConfigMaps and Secrets, and package and manage an Express application using Helm.", body_style))
    story.append(Paragraph("<b>Core Lab Objectives:</b>", body_style))
    for item in [
        "Build and load a multi-stage Node.js and Express container image (<code>student-app:1.0.0</code>) across cluster nodes.",
        "Run a finite Kubernetes <code>Job</code> (<code>batch/v1</code>) to completion and inspect Pod logs and retry behaviour.",
        "Deploy a scheduled <code>CronJob</code>, observe automatic Job creation, and test suspension and resumption.",
        "Inject non-sensitive settings with a <code>ConfigMap</code> and verify the need for a Pod restart when env vars change.",
        "Inject dummy credentials with a <code>Secret</code> and verify presence safely without exposing credential values.",
        "Author a custom Helm chart and perform <code>helm lint</code>, <code>template</code>, <code>install</code>, <code>upgrade</code>, <code>history</code>, and <code>rollback</code>.",
    ]:
        story.append(Paragraph(f"&bull; {item}", bullet_style))

    story.append(Paragraph("2. Project Architecture and Structure", h1_style))
    story.append(Paragraph("All Lab 6 resources run in the isolated namespace <code>devops-lab6</code>. Application source code resides under <code>Lab-6/app/</code>, batch manifests under <code>Lab-6/jobs/</code>, standalone manifests under <code>Lab-6/kubernetes/</code>, and the custom Helm chart under <code>Lab-6/helm/student-app/</code>. Previous Lab 5 files remain unmodified on branch history.", body_style))
    story.append(make_figure(
        "01-project-structure.png",
        "Figure 1: Organized Lab-6 directory structure verified on the Killercoda controlplane node.",
        "Confirmed clean separation between container source, Jobs/CronJobs, Kubernetes manifests, and Helm chart templates.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 4. DOCKER IMAGE PREPARATION
    # =========================================================================
    story.append(Paragraph("3. Docker Image Preparation", h1_style))
    story.append(Paragraph("A multi-stage <code>Dockerfile</code> built <code>student-app:1.0.0</code> from <code>node:20-alpine</code>, running as unprivileged user <code>node</code> on port <code>8080</code> with endpoints <code>/healthz</code>, <code>/ready</code>, <code>/config</code>, and <code>/secret-status</code>. Because the Killercoda cluster uses two nodes running <code>containerd://2.2.1</code>, the built image was exported with <code>docker save</code> and imported into containerd's <code>k8s.io</code> namespace on both <code>controlplane</code> and <code>node01</code>.", body_style))
    story.append(Paragraph("<code>docker build -t student-app:1.0.0 ./app &amp;&amp; docker run -d --rm -p 18080:8080 --name test-app student-app:1.0.0 &amp;&amp; curl -s http://127.0.0.1:18080/healthz</code>", code_style))
    story.append(make_figure(
        "02-docker-image-build.png",
        "Figure 2: Multi-stage Docker image build (138MB), image listing, and direct /healthz container verification.",
        "Image 23f204777f0d built cleanly and returned HTTP 200 JSON (status UP) before containerd import onto both cluster nodes.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 5. KUBERNETES JOB IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("4. Kubernetes Job Implementation", h1_style))
    story.append(Paragraph("Created <code>jobs/job.yaml</code> (<code>student-batch-report-job</code>, <code>apiVersion: batch/v1</code>, <code>restartPolicy: Never</code>, <code>backoffLimit: 3</code>) in namespace <code>devops-lab6</code>. Rather than sleeping, the container processes 500 simulated student score records, computes pass counts and average score, writes <code>/tmp/batch-report.json</code>, and outputs a SHA-256 checksum.", body_style))
    story.append(make_figure(
        "03-job-yaml.png",
        "Figure 3: Job manifest (jobs/job.yaml) configuring completions, parallelism, backoffLimit, and restartPolicy.",
        "Verified batch/v1 Job configuration with finite completion target (1/1) and non-restarting Pod failure policy.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "04-job-completed.png",
        "Figure 4: Job creation, Complete (1/1) status, Completed Pod state, and Job controller events.",
        "student-batch-report-job spawned pod student-batch-report-job-wlnfl and reached Complete (1/1) in 7 seconds.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "05-job-logs.png",
        "Figure 5: Retrieved Pod logs confirming batch computation and checksum output.",
        "kubectl logs recorded 500 processed records, 444 passed, averageScore 76.94, and checksum 18e4cc52de0e.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 6. KUBERNETES CRONJOB IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("5. Kubernetes CronJob Implementation", h1_style))
    story.append(Paragraph("Created <code>jobs/cronjob.yaml</code> (<code>periodic-audit-cronjob</code>) with temporary test schedule <code>* * * * *</code>, <code>concurrencyPolicy: Forbid</code>, <code>startingDeadlineSeconds: 60</code>, <code>successfulJobsHistoryLimit: 3</code>, <code>failedJobsHistoryLimit: 1</code>, and <code>restartPolicy: OnFailure</code>. While a Job executes once, a CronJob creates a new Job object automatically whenever its cron schedule triggers.", body_style))
    story.append(make_figure(
        "06-cronjob-yaml.png",
        "Figure 6: CronJob manifest defining schedule, concurrencyPolicy: Forbid, and job history limits.",
        "Verified declarative schedule fields and non-overlapping concurrency policy prior to cluster deployment.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "07-cronjob-scheduled-execution.png",
        "Figure 7: Scheduled CronJob triggering Job periodic-audit-cronjob-29927292, Completed Pod, and JSON audit logs.",
        "CronJob controller scheduled job 29927292 on the minute mark; pod p9bc7 completed in 3s logging auditStatus: OK.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 7. CONFIGMAP IMPLEMENTATION AND VERIFICATION
    # =========================================================================
    story.append(Paragraph("6. ConfigMap Implementation and Verification", h1_style))
    story.append(Paragraph("Created <code>kubernetes/configmap.yaml</code> (<code>student-app-config</code>) to store five non-sensitive settings: <code>APP_NAME</code>, <code>APP_ENV</code>, <code>LOG_LEVEL</code>, <code>APP_MODE</code>, and <code>PUBLIC_MESSAGE</code>. Injected these into <code>student-config-demo</code> via <code>envFrom.configMapRef</code>.", body_style))
    story.append(make_figure(
        "08-configmap-creation.png",
        "Figure 8: Applying kubernetes/configmap.yaml and inspecting keys via kubectl describe configmap.",
        "Confirmed all five non-sensitive configuration keys stored cleanly in devops-lab6.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "09-configmap-injection.png",
        "Figure 9: ConfigMap update verification showing new LOG_LEVEL (debug) and PUBLIC_MESSAGE after rollout restart.",
        "Updating the ConfigMap left the initial Pod (2mr7s) serving logLevel: info; only after kubectl rollout restart did new Pod 649lh serve logLevel: debug.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 8. SECRET IMPLEMENTATION AND VERIFICATION
    # =========================================================================
    story.append(Paragraph("7. Secret Implementation and Verification", h1_style))
    story.append(Paragraph("Created an <code>Opaque</code> Kubernetes Secret (<code>app-credentials</code>) using dummy demonstration keys (<code>APP_USERNAME</code> and <code>APP_PASSWORD</code>) loaded from a temporary env-file deleted immediately afterward so credential literals never appeared in shell logs or Git. Important: Kubernetes Secret values are base64-encoded, and <b>base64 is encoding, not encryption</b>.", body_style))
    story.append(make_figure(
        "10-secret-creation.png",
        "Figure 10: Safe Secret inspection displaying key names and byte sizes without exposing credential values.",
        "kubectl describe secret app-credentials shows metadata and key byte sizes (13 bytes, 9 bytes) cleanly without revealing values.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "11-secret-reference-in-pod.png",
        "Figure 11: Pod secretKeyRef injection check and masked /secret-status application response.",
        "Pod events/env references confirm app-credentials keys are attached, and /secret-status returns secretConfigured: true with values redacted.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 9. HELM CHART CREATION AND INSTALLATION
    # =========================================================================
    story.append(Paragraph("8. Helm Chart Creation and Installation", h1_style))
    story.append(Paragraph("Built a custom Helm v2 chart at <code>Lab-6/helm/student-app/</code> with <code>Chart.yaml</code>, <code>values.yaml</code>, <code>values-dev.yaml</code>, and templates (<code>_helpers.tpl</code>, <code>configmap.yaml</code>, <code>deployment.yaml</code>, <code>service.yaml</code>, <code>NOTES.txt</code>). No passwords are stored in <code>values.yaml</code>; instead, <code>deployment.yaml</code> references the externally created Secret <code>app-credentials</code> and computes a <code>checksum/config</code> annotation so ConfigMap edits trigger automatic rolling updates during Helm upgrades.", body_style))
    story.append(make_figure(
        "12-helm-chart-structure.png",
        "Figure 12: Custom Helm chart layout and Chart.yaml metadata (chart version 0.1.0, appVersion 1.0.0).",
        "Chart directory follows standard Helm v2 packaging structure.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "12b-helm-values.png",
        "Figure 13: values.yaml showing NodePort 30086, resource limits, config values, and external secretRef.",
        "Sensitive credentials stay externalized under secretRef.name: app-credentials.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "12c-helm-deployment-template.png",
        "Figure 14: Deployment template illustrating checksum/config annotation, envFrom, and Downward API variables.",
        "Helm templates render consistent labels and rolling update checksums dynamically.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "13-helm-lint.png",
        "Figure 15: Validation via helm lint and helm template rendering Kubernetes YAML manifests.",
        "helm lint returned '1 chart(s) linted, 0 chart(s) failed' and helm template output valid ConfigMap, Service, and Deployment YAML.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "14-helm-install.png",
        "Figure 16: Installing release student-app and verifying deployed status, 2/2 Running Pods, and NodePort 30086.",
        "helm install created Revision 1 (deployed) with 2 healthy pods (kf59l, w5fcd) exposed on Service student-app-svc.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "15-application-browser.png",
        "Figure 17: Live Chrome browser view of the deployed application accessed through Killercoda NodePort 30086.",
        "Browser displayed baseline production-helm config, Pod kf59l metadata, HTTP 200 health probe, and masked Secret confirmation.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 10. HELM UPGRADE AND ROLLBACK
    # =========================================================================
    story.append(Paragraph("9. Helm Upgrade and Rollback", h1_style))
    story.append(Paragraph("Upgraded the release using <code>-f ./helm/student-app/values-dev.yaml</code> (increasing replicas from 2 to 3 and changing ConfigMap settings to <code>development-override</code> and <code>debug</code>), inspected revision history, and rolled back cleanly to Revision 1. Unlike <code>kubectl rollout undo</code>—which reverts only a single Deployment's Pod template—<code>helm rollback</code> restores the entire release manifest bundle (ConfigMap, Service, and Deployment together) as a new revision.", body_style))
    story.append(make_figure(
        "16-helm-upgrade.png",
        "Figure 18: Executing helm upgrade with values-dev.yaml, scaling to 3/3 Pods and updating /config.",
        "Helm incremented the release to Revision 2, scaled Pods to 3/3 (56gtj, pn5td, z5vh7), and applied development-override config.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "16b-application-browser-upgraded.png",
        "Figure 19: Refreshed Chrome browser showing upgraded development-override environment and debug log level.",
        "Browser UI reflected Revision 2 changes served from pod student-app-78867d8cc5-pn5td while keeping secrets redacted.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "17-helm-history.png",
        "Figure 20: Helm revision history showing Revision 1 (superseded) and Revision 2 (deployed).",
        "helm history accurately recorded release progression across install and upgrade.",
        body_style, cap_style, obs_style, target_width=405,
    ))
    story.append(make_figure(
        "18-helm-rollback.png",
        "Figure 21: Executing helm rollback student-app 1, creating Revision 3 and restoring 2 Pods and baseline config.",
        "Rollback restored replica count to 2/2 (5xlpf, 8fj79) and reverted /config back to production-helm (logLevel: info).",
        body_style, cap_style, obs_style, target_width=405,
    ))

    # =========================================================================
    # 11. SELF-LEARNING PRACTICAL DEMONSTRATIONS
    # =========================================================================
    story.append(Paragraph("10. Self-Learning Practical Demonstrations", h1_style))
    story.append(Paragraph("<b>Enhancement A — Job Retry and backoffLimit Behaviour:</b> Applied <code>jobs/job-retry-test.yaml</code> (exiting with status 1 and <code>backoffLimit: 2</code>). Verified all Pod attempts, events, and logs, then deleted the failed test Job cleanly.", body_style))
    story.append(make_figure(
        "19-job-retry-test.png",
        "Figure 22: Controlled failure demonstration showing 3 failed Pods and BackoffLimitExceeded event.",
        "Kubernetes attempted 1 initial Pod (x6mtr) plus 2 retries (qgpc9, strbz) before stopping retries and marking the Job Failed (0/1).",
        body_style, cap_style, obs_style, target_width=405,
    ))

    story.append(Paragraph("<b>Enhancement B — CronJob Suspension, Concurrency Policy and Resumption:</b> With <code>concurrencyPolicy: Forbid</code> active, patched <code>periodic-audit-cronjob</code> to <code>suspend: true</code>, observed 0 new Jobs created over a 65-second interval spanning a minute tick, resumed with <code>suspend: false</code>, confirmed new Job <code>29927293</code> started, and re-suspended afterward so idle test Jobs would not accumulate.", body_style))
    story.append(make_figure(
        "20-cronjob-controls-test.png",
        "Figure 23: Testing CronJob suspend=true (0 new Jobs in 65s) followed by suspend=false triggering Job 29927293.",
        "Verified suspend halts scheduling cleanly without deleting the CronJob, and resume restores scheduled execution.",
        body_style, cap_style, obs_style, target_width=405,
    ))

    story.append(Paragraph("<b>Enhancement C — Helm Values Override Upgrade &amp; Full Release Rollback:</b> Executed end-to-end in Section 9 (Figures 18–21) using <code>values-dev.yaml</code> overrides, <code>checksum/config</code> rollout propagation, <code>helm history</code> tracking, and <code>helm rollback student-app 1</code> verification.", body_style))

    # =========================================================================
    # 12. VERIFICATION TEST MATRIX
    # =========================================================================
    story.append(Paragraph("11. Verification Test Matrix", h1_style))
    matrix = [
        [Paragraph("<b>Requirement</b>", body_style), Paragraph("<b>Command / Test Executed</b>", body_style), Paragraph("<b>Actual Observed Result</b>", body_style), Paragraph("<b>Status</b>", body_style)],
        [Paragraph("Docker build", body_style), Paragraph("<code>docker build</code> + <code>curl /healthz</code>", body_style), Paragraph("138MB image built, HTTP 200 UP", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Job completion &amp; logs", body_style), Paragraph("<code>kubectl apply -f jobs/job.yaml</code>", body_style), Paragraph("Complete (1/1) in 7s; 500 records logged", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Job retry test", body_style), Paragraph("<code>kubectl apply -f jobs/job-retry-test.yaml</code>", body_style), Paragraph("3 failed Pods, BackoffLimitExceeded, deleted", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("CronJob execution", body_style), Paragraph("<code>kubectl apply -f jobs/cronjob.yaml</code>", body_style), Paragraph("Job 29927292 created &amp; Complete (1/1)", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("CronJob suspend/resume", body_style), Paragraph("<code>kubectl patch cj ... suspend</code>", body_style), Paragraph("0 Jobs in 65s suspended; 29927293 on resume", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("ConfigMap injection", body_style), Paragraph("<code>kubectl patch cm</code> + <code>rollout restart</code>", body_style), Paragraph("/config changed from info to debug post-restart", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Secret injection", body_style), Paragraph("<code>kubectl create secret</code> + <code>/secret-status</code>", body_style), Paragraph("2 keys injected, values never exposed", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Helm lint &amp; template", body_style), Paragraph("<code>helm lint</code> &amp; <code>helm template</code>", body_style), Paragraph("0 chart failures, valid YAML rendered", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Helm install &amp; browser", body_style), Paragraph("<code>helm install</code> + Chrome :30086", body_style), Paragraph("Rev 1 deployed (2/2 Pods), UI verified live", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Helm upgrade", body_style), Paragraph("<code>helm upgrade -f values-dev.yaml</code>", body_style), Paragraph("Rev 2 deployed (3/3 Pods), dev UI verified", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
        [Paragraph("Helm history &amp; rollback", body_style), Paragraph("<code>helm rollback student-app 1</code>", body_style), Paragraph("Rev 3 Rollback to 1; 2/2 Pods &amp; baseline restored", body_style), Paragraph("<font color='#059669'><b>PASS</b></font>", body_style)],
    ]
    t_mat = Table(matrix, colWidths=[110, 145, 192, 55])
    t_mat.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (-1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(t_mat)

    # =========================================================================
    # 13. CONCLUSION & 14. REFERENCES
    # =========================================================================
    story.append(Paragraph("12. Conclusion", h1_style))
    story.append(Paragraph("Lab Exercise 6 successfully verified Kubernetes workload automation, configuration separation, and Helm release management against a live two-node Kubernetes v1.37.1 cluster. Finite and scheduled tasks were verified through Jobs and CronJobs (including retry limits and schedule suspension), non-sensitive and dummy sensitive data were safely separated across ConfigMaps and Secrets, and the Node.js application was packaged, linted, installed, upgraded via override values, and rolled back cleanly using Helm v4.3.0.", body_style))

    story.append(Paragraph("13. References", h1_style))
    story.append(Paragraph(
        "1. Kubernetes Official Documentation — Jobs &amp; CronJobs: <i>https://kubernetes.io/docs/concepts/workloads/controllers/job/</i><br/>"
        "2. Kubernetes Official Documentation — ConfigMaps &amp; Secrets: <i>https://kubernetes.io/docs/concepts/configuration/</i><br/>"
        "3. Helm Official Documentation — Charts, Templates &amp; Rollbacks: <i>https://helm.sh/docs/</i><br/>"
        "4. Course Reference Repository: <i>https://github.com/vellankikoti/docker-k8s-zero-to-hero</i>",
        ParagraphStyle("Ref", fontName="Helvetica", fontSize=8, leading=11.5, textColor=colors.HexColor("#475569")),
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF compiled successfully at: {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
