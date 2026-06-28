# 文獻月報整合 — 2026 年 5 月

跨三份專科月報（ERCP、肝硬化、脂肪肝）的整合視圖。原始檔案來自 Google Drive
*journal reading* 資料夾，已同步為 `data/external/reading_list.csv`（gitignored）。
本頁為版控保存的整合結果。

- **涵蓋期間：** 2026-05-01 – 2026-05-31（含少數近月延續性證據）
- **產生流程：** 搜尋員 → 報告員 → 研究方法檢查員；來源限權威同儕審查期刊，
  排除掠奪性期刊；全文經北榮 ERMG/EDS proxy enrich。
- **重建方式：** `scripts/integrate_monthly_reports.py`（統計＋圖表）、
  `scripts/analyze_reading_list.py`（摘要）。

## 總覽統計

| report | AI | general | 總計 |
|--------|----|---------|------|
| ERCP | 0 | 14 | 14 |
| 肝硬化 | 15 | 15 | 30 |
| 脂肪肝 | 15 | 15 | 30 |
| **總計** | **30** | **44** | **74** |

- **總列數 74、去重後唯一論文 72**（依 PMID）。
- **跨月報重複 2 篇**（肝硬化與脂肪肝同時收錄）：
  - `42065864` — belapectin NAVIGATE trial（MASH 肝硬化／藥物）
  - `42291159` — FibroX 機器學習纖維化模型（MASLD／AI）

### 收錄最多的期刊（唯一論文）

| 期刊 | 篇數 |
|------|------|
| Clin Gastroenterol Hepatol | 7 |
| Hepatology | 5 |
| Front Oncol | 5 |
| Front Med | 4 |
| Aliment Pharmacol Ther | 4 |
| J Hepatol | 4 |
| Liver Int | 4 |
| Gut | 3 |
| J Clin Med | 3 |
| Hepatol Int | 3 |

圖表輸出於 `outputs/`：`monthly_by_report_section.png`、`monthly_top_journals.png`
（gitignored，執行上述腳本後產生）。

## 各月報旗艦研究

- **ERCP — *Gut* 急性膽管炎時機 RCT（PMID 42161575）**：輕中度急性膽管炎，
  24h 內緊急 ERCP 未較 24–48h 早期降低 30 天死亡，且術後出血較高；
  因提前停收而 underpowered（power ~18%），結論為「未優於」而非等效。
- **肝硬化 — 非顯影 AMRI 監測 HCC（PMID 42113186）**：AMRI 對 HCC 敏感度
  94.6% vs 超音波 51.4%，AUROC 0.956 vs 0.604；檢出之 HCC 97% 為早期。
- **脂肪肝 — 全球 HCC 病因歸因統合分析（*Gut*, PMID 42135055）**：HBV+HCV 合計
  佔全球肝癌約 75%；歐洲/南美部分國家 >30% 與酒精/MASLD 相關。

## 跨月報共通主題

- **AI／radiomics 大量湧現但證據力受限**：肝硬化與脂肪肝各 15 篇 AI 論文，
  方法檢查普遍指出單中心、回溯、缺外部驗證、AUC 可能過度樂觀（過度擬合）。
- **藥物試驗交集**：belapectin（NAVIGATE）同時出現在肝硬化與脂肪肝月報，
  反映 MASH 肝硬化是兩科交界；主要終點未達顯著、陽性僅見於 per-protocol 次族群。
- **非侵入診斷是熱點**：TSP2 生物標記、AMRI、cfDNA 血檢、彈性造影 radiomics。
- **證據誠實度**：三份月報皆明確標註「延續性證據」月份、全文 enrich 狀態與
  underpowered/選擇偏差等限制，未誇大結論。

## 統一文獻清單

PMID 連結格式：`https://pubmed.ncbi.nlm.nih.gov/<PMID>/`。空白 PMID 者原月報僅提供 DOI。

### ERCP（14）

| PMID | 標題 | 期刊 | 面向 |
|------|------|------|------|
| 42161575 | Urgent vs early ERCP in mild-to-moderate acute cholangitis (RCT) | Gut | 時機/適應症 |
| 42203288 | STRIPE: five-arm RCT protocol (IV fluids for PEP prevention) | BMJ Open | PEP預防 |
| 42194902 | Post-ERCP Pancreatitis and New-Onset Diabetes (cohort) | J Clin Med | PEP後遺 |
| 42194876 | Preventing Post-ERCP Pancreatitis: A Pragmatic Clinical Pathway | J Clin Med | PEP預防 |
| — | Rectal Diclofenac vs Indomethacin for PEP (meta-analysis) | Dig Dis Sci | PEP預防 |
| 42351482 | AI-Based Prediction of Post-ERCP Pancreatitis | Diagnostics | AI |
| 42349763 | Metallic stents 10- vs 14-mm for distal biliary obstruction (RCT) | Gastrointest Endosc | 惡性膽道支架 |
| — | FCSEMS removal vs stent-in-stent (recurrent MDBO) | Sci Rep | 惡性膽道支架 |
| 42344412 | Biliary cannulation success after transpancreatic precut | Endosc Int Open | 困難插管 |
| 42253372 | Post-ERCP Outcomes in Cirrhotic Patients With Thrombocytopenia | JGH Open | 特殊族群 |
| 42180735 | Dexmedetomidine nasal spray + propofol for ERCP sedation (RCT) | Front Med | 鎮靜/麻醉 |
| 42194633 | Entropy-Guided Sedation During ERCP | J Clin Med | 鎮靜/麻醉 |
| 42195206 | Prevalence of Pancreas Divisum (meta-analysis) | Medicina | 解剖學 |
| 42168374 | Music intervention on ERCP patients (RCT) | Sci Rep | 病人經驗 |

### 肝硬化 — 一般（15）

| PMID | 標題 | 期刊 | 面向 |
|------|------|------|------|
| 42065864 | Belapectin for prevention of esophageal varices (NAVIGATE) | Hepatology | 併發症(靜脈曲張) |
| 42092293 | Rifaximin for covert hepatic encephalopathy (RCT) | Aliment Pharmacol Ther | 併發症(肝性腦病) |
| 42213313 | Tolvaptan for hyponatremia in cirrhosis (post hoc) | Hepatol Int | 併發症(低血鈉) |
| 42107856 | Terlipressin in HRS — HRS Harmony Consortium | Clin Gastroenterol Hepatol | 併發症(肝腎症候群) |
| 42113186 | Noncontrast AMRI vs ultrasound for HCC detection | Hepatology | HCC監測 |
| 42102976 | Multi-analyte cfDNA blood test for early HCC | J Hepatol | HCC監測 |
| 42129064 | SBP-INDIA: AMR & empiric treatment for SBP | Aliment Pharmacol Ther | 併發症(SBP) |
| 42207228 | Multisociety consensus on PSVD / NCPF | J Hepatol | 病理機制/指引 |
| 42208783 | Noninvasive prediction of decompensation (LSM 15–25 kPa) | Clin Gastroenterol Hepatol | 診斷/門脈高壓 |
| 42119851 | Rifaximin ameliorates portal hypertension via DCA suppression | J Hepatol | 病理機制 |
| 42107855 | Frailty increases hospitalization — NACSELD3 | Clin Gastroenterol Hepatol | 流行病學/預後 |
| 42171974 | ICI for advanced HCC in CTP-B cirrhosis | Hepatol Int | HCC治療 |
| 42198836 | Socioeconomic inequalities in surveillance-detected HCC | Aliment Pharmacol Ther | 流行病學/HCC監測 |
| 42010744 | Albumin restores endothelial mitochondrial morphology | Liver Int | 病理機制 |
| 42007664 | Primary haemostasis in cirrhosis with bacterial infection | Liver Int | 併發症(感染) |

### 肝硬化 — AI（15）

| PMID | 標題 | 期刊 | 面向 |
|------|------|------|------|
| 42174361 | ML outperforms creatinine for HRS risk stratification | Hepatol Int | AI/HRS |
| 42291159 | FibroX: ML model for advanced fibrosis in MASLD | Transl Gastroenterol Hepatol | AI/纖維化 |
| 42292236 | ML risk prediction of overt HE after TIPS | Front Med | AI/肝性腦病 |
| 42294337 | AI in TACE for HCC (review) | Front Oncol | AI/HCC治療 |
| 42294279 | DDVD radiomics: HCC vs hemangioma | Front Oncol | AI/HCC診斷 |
| 42285885 | Delta radiomics for HCC prognosis after TACE | Hepatobiliary Pancreat Dis Int | AI/HCC預後 |
| 42272655 | Radiomics + habitat for HCC recurrence post-transplant | Front Oncol | AI/HCC移植 |
| 42255247 | CT habitat imaging for MVI in HCC | Front Oncol | AI/HCC診斷 |
| 42239509 | CT radiomics + circulating tumor cells for HCC survival | Front Pharmacol | AI/HCC預後 |
| 42245726 | The translational paradox of AI in HCC (review) | Front Oncol | AI/方法學 |
| 42325785 | ML for length of stay in decompensated cirrhosis | Am J Transl Res | AI/預後 |
| 42218308 | ML comparison of MELD / MELD-Na / MELD 3.0 in HCC | Dig Dis Sci | AI/HCC預後 |
| 42311287 | ML-assisted SERS for liver fibrosis diagnosis | Biomed Opt Express | AI/纖維化 |
| 42325764 | US/elastography radiomics for HCC recurrence & MVI | Am J Transl Res | AI/HCC診斷 |
| 42254389 | CT radiomics + inflammatory indicators for first TACE | Front Med | AI/HCC治療 |

### 脂肪肝 — 一般（15）

| PMID | 標題 | 期刊 | 面向 |
|------|------|------|------|
| 42135055 | Global HCC attributable to HBV/HCV/other (meta-analysis) | Gut | 流行病學 |
| 40935097 | HCC incidence in MASLD (reconstructed IPD meta-analysis) | Clin Gastroenterol Hepatol | 流行病學 |
| 42218732 | Prevalence of at-risk MASH & advanced fibrosis in primary care | Aliment Pharmacol Ther | 流行病學 |
| 42292774 | Steatotic liver disease among people with HIV in Uganda | Open Forum Infect Dis | 流行病學 |
| 40972880 | Cardiometabolic risk factors & mortality in MASLD (NHANES) | Clin Gastroenterol Hepatol | 流行病學 |
| 42255423 | SLD subtype & thyroid cancer in women (nationwide cohort) | Front Endocrinol | 流行病學 |
| 42221460 | Metabolic multimorbidity & mortality in HIV (China) | Lancet Reg Health West Pac | 共病與心血管 |
| 42065864 | Belapectin NAVIGATE trial (MASH cirrhosis) | Hepatology | 藥物治療 |
| 42127430 | Efruxifermin across PNPLA3 genotypes in MASH (phase 2b) | Hepatology | 藥物治療 |
| 41201884 | Semaglutide for MASH — AASLD Practice Guidance update | Hepatology | 指引與方法學 |
| 42167630 | Hepatic steatosis & adverse coronary plaque (PROMISE) | Clin Gastroenterol Hepatol | 共病與心血管 |
| 40738743 | Thrombospondin-2 biomarker for at-risk MASH/fibrosis | Gut | 診斷與非侵入檢測 |
| 42134753 | Fibrosis progression: biopsy vs NIT in MetALD/ALD | Clin Gastroenterol Hepatol | 診斷與非侵入檢測 |
| 42191458 | EASL position paper on preclinical SLD models | J Hepatol | 病理機制 |
| 40720744 | Chiglitazar in MASLD with hypertriglyceridemia (phase II) | Hepatology | 藥物治療 |

### 脂肪肝 — AI（15）

| PMID | 標題 | 期刊 | 面向 |
|------|------|------|------|
| 42291159 | FibroX: ML for advanced fibrosis in MASLD | Transl Gastroenterol Hepatol | AI/風險預測 |
| 42291168 | Narrative review of AI in MASLD diagnosis & management | Transl Gastroenterol Hepatol | AI/綜述 |
| 42207764 | ML prediction of HCC risk in SLD (nationwide cohort) | PLoS One | AI/風險預測 |
| 41947638 | Point-of-care transient elastography with integrated AI | Liver Int | AI/影像診斷 |
| 41943460 | Radiomics for portal hypertension severity (routine CT) | Liver Int | AI/影像診斷 |
| 42132499 | Automated CT steatosis risk for deceased organ donors | Transplantation | AI/影像診斷 |
| 42141301 | Explainable ML using routine labs for prevalent MASLD | Clin Exp Med | AI/風險預測 |
| 42193478 | ML for ultrasound-detected hepatic steatosis | Biomedicines | AI/風險預測 |
| 42222087 | ML for coronary heart disease in T2DM + MASLD | Front Endocrinol | AI/風險預測 |
| 42229200 | Phenotyping ED patients with incidental steatosis (LLM+ML) | Am J Emerg Med | AI/風險預測 |
| 42292193 | AutoML for colorectal adenoma in MASLD | Front Med | AI/風險預測 |
| 42178484 | Multiparametric MRI radiomics for MAFLD fibrosis (rat) | Medical Physics | AI/影像診斷 |
| 42141448 | ML for NAFLD risk in sleep apnea (multicenter) | BMC Med Inform Decis Mak | AI/風險預測 |
| 42135651 | Liver CT composite biomarkers for MASH pre-bariatric | BMC Gastroenterol | AI/影像診斷 |
| 42196855 | Hepatic fat quantification via probabilistic neural network | Diagnostics | AI/影像診斷 |

---

*本整合頁由 `data/external/reading_list.csv` 機械彙整而成；論文數據請以原月報與 PubMed
原文為準。原月報已標註各篇方法限制與證據等級。*
