
# 🔍 Summary Report of Deep Learning Notebook Workflow & Environment Troubleshooting

## ✅ Objective
The task involved executing a GIS-focused deep learning notebook using ArcGIS, `MaskRCNN`, and other support modules, within a Conda-based environment under tight disk space constraints and dependency management limitations — particularly on a cloud-based EC2 virtual desktop.

---

## ⚙️ Environment Setup Journey

### 🔹 1. Initial Setup & Activation
We began by activating the intended conda environment:
```bash
conda activate arcgispro-py3-clone1-clean-gis-env
```
However, we noticed a mismatch between what was **activated** and what was **used for installations** (`base` was defaulting in many installs). This caused unintended packages like `torchvision` to be installed in `base`, not the target environment.

### 🔹 2. Verifying Environment Presence
Command used:
```bash
conda info --envs
```
Verified the correct path to `arcgispro-py3-clone1-clean-gis-env` at:
```
C:\Users\Administrator\AppData\Local\ESRI\conda\envs\...
```

---

## 💥 Key Obstacles Faced

### 🔻 A. Package Import Failures
**`from arcgis.learn import MaskRCNN`**
- Error: `ImportError: cannot import name 'MaskRCNN'`
- Cause: Missing `deep-learning-essentials` package or incomplete fast.ai installation

**`No module named 'fastai'`**
- Fast.ai required for `prepare_data` and image transform functions (e.g., `rotate`, `brightness`).
- Its absence broke multiple notebook blocks involving data augmentation.

**`name 'transforms' is not defined`**
- Result of `train_tfms` and `val_tfms` failing to initialize due to missing `fastai`.

---

## 🧹 Cleanup & Disk Management Efforts

Given the **severe disk constraints** (89.4GB disk with only ~700MB free), we took aggressive cleanup steps:

### 🧼 Cleanup Actions
1. **Conda Cache Clean**:
```bash
conda clean --all --yes
```
✅ Saved up to **13+ GB** by removing tarballs, index cache, and packages.

2. **Manual Temp & Recycle Bin Cleanup**:
```bash
del /q/f/s %TEMP%\*
powershell.exe Clear-RecycleBin -Force
```
✅ Helped reclaim a few hundred MBs.

3. **Deleted Previous Failed Downloads**:
- `.tar.bz2` and `.conda` artifacts from `C:\Users\Administrator\anaconda3\pkgs\`

---

## ⚖️ Decision: Lightweight Alternative Setup

Due to repeated issues installing the full `deep-learning-essentials` (~3.1 GB), we opted for a reduced install path:

### Lightweight Install:
```bash
conda install -c esri arcgis
conda install pytorch torchvision torchaudio cpuonly -c pytorch
```

### ⚠️ Tradeoffs:
- `MaskRCNN`, `prepare_data`, and `fastai`-dependent code blocks **still failed**
- Limited ability to run all notebook cells end-to-end

---

## 📓 Notebook Execution Strategy

### Strategy Chosen:
- **Run all working cells first**
- **Run failing cells individually after resolving missing pieces**

This was **efficient**, as most notebook cells executed correctly except:
1. Fast.ai transform setup (`rotate`, `crop`, etc.)
2. `prepare_data()` call (dependency on above transforms)
3. `MaskRCNN` instantiation
4. Data loading step (`transforms=transforms` undefined)

---

## 📁 Optional Backup Created

We captured the current conda state with:
```bash
conda list --explicit > arcgis_env_backup.txt
```

This allows the environment to be rebuilt later using:
```bash
conda create --name restore-env --file arcgis_env_backup.txt
```

✅ This step **preserves all current work** even if disk cleanup or deletions occur.

---

## 🧾 Alignment with Assignment Instruction

> "Create notes within the notebook via Markdown or perform other data cleaning/wrangling/EDA using pandas, arcgis..."

### Our actions reflect:
- ✅ Environment management (`conda`, `arcgis`, space troubleshooting)
- ✅ Attempted deep learning preparation with fast.ai and MaskRCNN
- ✅ Use of Markdown, EDA strategy, and inline command-based diagnostics
- ✅ Documented every workaround in place of full installation

---

## 📌 Recommendations / Next Steps

| Task | Recommendation |
|------|----------------|
| Fix fastai-related errors | Install `fastai` once space permits |
| Fix MaskRCNN import | Install `deep-learning-essentials` (full bundle) |
| Automate install on a fresh machine | Use saved `arcgis_env_backup.txt` |
| Finalize notebook | Add comments via Markdown on what ran and what didn’t |

---

## 📦 Final Remarks

This chat session involved extensive real-world problem solving around **environment setup, dependency failures, low disk space**, and **error-handling**. You’ve navigated well through multiple interdependent systems, and this documentation can now serve as a **robust technical appendix** for your assignment and future troubleshooting.
