---
annotations_creators:
- expert-generated
language_creators:
- expert-generated
languages:
- en
licenses:
- apache-2.0
multilinguality:
- monolingual
size_categories:
- 10K<n<100K
source_datasets:
- extended|other-MS^2
- extended|other-Cochrane
task_categories:
- summarization
- text2text-generation
task_ids:
- summarization-other-query-based-summarization 
- summarization-other-query-based-multi-document-summarization
- summarization-other-scientific-documents-summarization
paperswithcode_id: multi-document-summarization
pretty_name: MSLR Shared Task
---

# Dataset Card for MSLR2022

## Table of Contents
- [Dataset Card for MSLR2022](#dataset-card-for-mslr2022)
  - [Table of Contents](#table-of-contents)
  - [Dataset Description](#dataset-description)
    - [Dataset Summary](#dataset-summary)
    - [Supported Tasks and Leaderboards](#supported-tasks-and-leaderboards)
    - [Languages](#languages)
  - [Dataset Structure](#dataset-structure)
    - [Data Instances](#data-instances)
    - [Data Fields](#data-fields)
    - [Data Splits](#data-splits)
  - [Dataset Creation](#dataset-creation)
    - [Curation Rationale](#curation-rationale)
    - [Source Data](#source-data)
      - [Initial Data Collection and Normalization](#initial-data-collection-and-normalization)
      - [Who are the source language producers?](#who-are-the-source-language-producers)
    - [Annotations](#annotations)
      - [Annotation process](#annotation-process)
      - [Who are the annotators?](#who-are-the-annotators)
    - [Personal and Sensitive Information](#personal-and-sensitive-information)
  - [Considerations for Using the Data](#considerations-for-using-the-data)
    - [Social Impact of Dataset](#social-impact-of-dataset)
    - [Discussion of Biases](#discussion-of-biases)
    - [Other Known Limitations](#other-known-limitations)
  - [Additional Information](#additional-information)
    - [Dataset Curators](#dataset-curators)
    - [Licensing Information](#licensing-information)
    - [Citation Information](#citation-information)

## Dataset Description

- **Homepage:** https://github.com/allenai/mslr-shared-task
- **Repository:** https://github.com/allenai/mslr-shared-task
- **Paper:** https://aclanthology.org/2021.emnlp-main.594
- **Leaderboard:** https://github.com/allenai/mslr-shared-task#leaderboard
- **Point of Contact:** https://github.com/allenai/mslr-shared-task#contact-us

### Dataset Summary

The Multidocument Summarization for Literature Review (MSLR) Shared Task aims to study how medical evidence from different clinical studies are summarized in literature reviews. Reviews provide the highest quality of evidence for clinical care, but are expensive to produce manually. (Semi-)automation via NLP may facilitate faster evidence synthesis without sacrificing rigor. The MSLR shared task uses two datasets to assess the current state of multidocument summarization for this task, and to encourage the development of modeling contributions, scaffolding tasks, methods for model interpretability, and improved automated evaluation methods in this domain.

### Supported Tasks and Leaderboards

This dataset is used for the MSLR2022 Shared Task. For information on the shared task leaderboard, please refer [here](https://github.com/allenai/mslr-shared-task#leaderboard).

### Languages

English

## Dataset Structure

More information on dataset structure [here](https://github.com/allenai/mslr-shared-task#data-structure).

### Data Instances

__MS^2__

```json
{
  "review_id": "30760312",
  "pmid": [
    "22776744",
    "25271670",
    "3493740",
    "1863023",
    "16291984",
    "23984728",
    "23996433",
    "18466198",
    "12151469",
    "27400308",
    "16053970",
    "22922316",
    "11897647",
    "11597664",
    "4230647"
  ],
  "title": [
    "Improved Cell Survival and Paracrine Capacity of Human Embryonic Stem Cell-Derived Mesenchymal Stem Cells Promote Therapeutic Potential for Pulmonary Arterial Hypertension",
    "Adipose-derived stem cells attenuate pulmonary arterial hypertension and ameliorate pulmonary arterial remodeling in monocrotaline-induced pulmonary hypertensive rats",
    "Effect of bone marrow mesenchymal stem cells on experimental pulmonary arterial hypertension",
    "Survival in patients with primary pulmonary hypertension. Results from a national prospective registry.",
    "Sildenafil citrate therapy for pulmonary arterial hypertension.",
    "Macitentan and morbidity and mortality in pulmonary arterial hypertension.",
    "Long-term research of stem cells in monocrotaline-induced pulmonary arterial hypertension",
    "Safety and efficacy of autologous endothelial progenitor cells transplantation in children with idiopathic pulmonary arterial hypertension: open-label pilot study.",
    "Inhaled iloprost for severe pulmonary hypertension.",
    "Sildenafil reduces pulmonary vascular resistance in single ventricular physiology.",
    "Ambrisentan therapy for pulmonary arterial hypertension.",
    "Mesenchymal stem cell prevention of vascular remodeling in high flow-induced pulmonary hypertension through a paracrine mechanism.",
    "Continuous subcutaneous infusion of treprostinil, a prostacyclin analogue, in patients with pulmonary arterial hypertension: a double-blind, randomized, placebo-controlled trial.",
    "Effects of the dual endothelin-receptor antagonist bosentan in patients with pulmonary hypertension: a randomised placebocontrolled study",
    "SYRCLE\\u2019s risk of bias tool for animal studies"
  ],
  "abstract": [
    "Although transplantation of adult bone marrow mesenchymal stem cells ( BM-MSCs ) holds promise in the treatment for pulmonary arterial hypertension ( PAH ) , the poor survival and differentiation potential of adult BM-MSCs have limited their therapeutic efficiency . Here , we compared the therapeutic efficacy of human embryonic stem cell-derived MSCs ( hESC-MSCs ) with adult BM-MSCs for the treatment of PAH in an animal model . One week following monocrotaline (MCT)-induced PAH , mice were r and omly assigned to receive phosphate-buffered saline ( MCT group ) ; 3.0 \\u00d7 106 human BM-derived MSCs ( BM-MSCs group ) or 3.0 \\u00d7 106 hESC-derived MSCs ( hESC-MSCs group ) via tail vein injection . At 3 weeks posttransplantation , the right ventricular systolic pressure ( RVSP ) , degree of RV hypertrophy , and medial wall thickening of pulmonary arteries were lower= , and pulmonary capillary density was higher in the hESC-MSC group as compared with BM-MSC and MCT groups ( all p < 0.05 ) . At 1 week posttransplantation , the number of engrafted MSCs in the lungs was found significantly higher in the hESC-MSC group than in the BM-MSC group ( all p < 0.01 ) . At 3 weeks posttransplantation , implanted BM-MSCs were undetectable whereas hESC-MSCs were not only engrafted in injured pulmonary arteries but had also undergone endothelial differentiation . In addition , protein profiling of hESC-MSC- and BM-MSC-conditioned medium revealed a differential paracrine capacity . Classification of these factors into bioprocesses revealed that secreted factors from hESC-MSCs were preferentially involved in early embryonic development and tissue differentiation , especially blood vessel morphogenesis . We concluded that improved cell survival and paracrine capacity of hESC-MSCs provide better therapeutic efficacy than BM-MSCs in the treatment for PAH",
    "Abstract We investigated the effect of adipose-derived stem cells ( ADSCs ) transplantation effects on structural remodeling and pulmonary artery pressure in  monocrotaline (MCT)-induced pulmonary hypertensive rats . In the first experiment , 32 male Sprague-Dawley ( SD ) rats were r and omly divided into four groups ( n = 8/group ) : 3 ADSCs treated groups and normal control ( Ctrl ) . ADSCs were administered through the left jugular vein at 105 , 106 and 107 cells , respectively , and a cell density of 106cells/ml was shown to be optimal . The GFP-tagged ADSCs were identified in the lungs and differentiated into endothelial-like cells . In the second experiment , 96 male SD rats were r and omly divided into three groups ( n = 32/group ) : Ctrl , MCT-induced pulmonary arterial hypertension ( PAH ) , and PAH treated with ADSCs ( ADSCs ) . Two weeks post-MCT administration , the ADSCs group received 1 \\u00d7 106 ADSCs via the external jugular vein . Compared to PAH rats , mean pulmonary arterial pressure was decreased in rats at 1 , 2 , and 3 weeks after ADSCs-treatment ( 18.63 \\u00b1 2.15 mmHg versus 24.53 \\u00b1 2.90 mmHg ; 23.07 \\u00b1 2.84 mmHg versus 33.18 \\u00b1 2.30 mmHg ; 22.98 \\u00b1 2.34 mmHg versus 36.38 \\u00b1 3.28 mmHg , p < 0.05 ) . Meanwhile , the right heart hypertrophy index ( 36.2 1 \\u00b1 4.27 % versus 41.01 \\u00b1 1.29 % ; 39.47 \\u00b1 4.02 % versus 48.75 \\u00b1 2 .13 % ; 41.02 \\u00b1 0.9 % versus 50.52 \\u00b1 1.49 % , p < 0.05 , respectively ) , ratio of wall/lumen thickness , as well as the wall/lumen area were significantly reduced in PAH rats at these time points following ADSCs-treatment , as compared with untreated PAH rats . In summary , ADSCs may colonize the pulmonary arteries , attenuate pulmonary arterial hypertension and ameliorate pulmonary arterial remodeling",
    "The aim of the present study was to investigate the effect of bone marrow mesenchymal stem cell ( BMSC ) transp1antation on lung and heart damage in a rat model of monocrotaline (MCT)-induced pulmonary arterial hypertension ( PAH ) . The animals were r and omly divided into 3 groups : control , PAH  and  BMSC implantation  groups . Structural changes in the pulmonary vascular wall , such as the pulmonary artery lumen area ( VA ) and vascular area ( TAA ) were measured by hematoxylin and eosin ( H&E ) staining , and the hemodynamics were detected by echocardiography . Two weeks post-operation , our results demonstrated that sublingual vein injection of BMSCs significantly attenuated the pulmonary vascular structural and hemodynamic changes caused by pulmonary arterial hypertension . The mechanism may be executed via paracrine effects",
    "OBJECTIVE To characterize mortality in persons diagnosed with primary pulmonary hypertension and to investigate factors associated with survival . DESIGN Registry with prospect i ve follow-up . SETTING Thirty-two clinical centers in the United States participating in the Patient Registry for the Characterization of Primary Pulmonary Hypertension supported by the National Heart , Lung , and Blood Institute . PATIENTS Patients ( 194 ) diagnosed at clinical centers between 1 July 1981 and 31 December 1985 and followed through 8 August 1988 . MEASUREMENTS At diagnosis , measurements of hemodynamic variables , pulmonary function , and gas exchange variables were taken in addition to information on demographic variables , medical history , and life-style . Patients were followed for survival at 6-month intervals . MAIN RESULTS The estimated median survival of these patients was 2.8 years ( 95 % Cl , 1.9 to 3.7 years ) . Estimated single-year survival rates were as follows : at 1 year , 68 % ( Cl , 61 % to 75 % ) ; at 3 years , 48 % ( Cl , 41 % to 55 % ) ; and at 5 years , 34 % ( Cl , 24 % to 44 % ) . Variables associated with poor survival included a New York Heart Association ( NYHA ) functional class of III or IV , presence of Raynaud phenomenon , elevated mean right atrial pressure , elevated mean pulmonary artery pressure , decreased cardiac index , and decreased diffusing capacity for carbon monoxide ( DLCO ) . Drug therapy at entry or discharge was not associated with survival duration . CONCLUSIONS Mortality was most closely associated with right ventricular hemodynamic function and can be characterized by means of an equation using three variables : mean pulmonary artery pressure , mean right atrial pressure , and cardiac index . Such an equation , once vali date d prospect ively , could be used as an adjunct in planning treatment strategies and allocating medical re sources",
    "BACKGROUND Sildenafil inhibits phosphodiesterase type 5 , an enzyme that metabolizes cyclic guanosine monophosphate , thereby enhancing the cyclic guanosine monophosphate-mediated relaxation and growth inhibition of vascular smooth-muscle cells , including those in the lung . METHODS In this double-blind , placebo-controlled study , we r and omly assigned 278 patients with symptomatic pulmonary arterial hypertension ( either idiopathic or associated with connective-tissue disease or with repaired congenital systemic-to-pulmonary shunts ) to placebo or sildenafil  ( 20 , 40 , or 80 mg ) orally three times daily for 12 weeks . The primary end point was the change from baseline to week 12 in the distance walked in six minutes . The change in mean pulmonary-artery pressure and World Health Organization ( WHO ) functional class and the incidence of clinical worsening were also assessed , but the study was not powered to assess mortality . Patients completing the 12-week r and omized study could enter a long-term extension study . RESULTS The distance walked in six minutes increased from baseline in all sildenafil groups ; the mean placebo-corrected treatment effects were 45 m ( + 13.0 percent ) , 46 m ( + 13.3 percent ) , and 50 m ( + 14.7 percent ) for 20 , 40 , and 80 mg of sildenafil , respectively ( P<0.001 for all comparisons ) . All sildenafil doses reduced the mean pulmonary-artery pressure ( P=0.04 , P=0.01 , and P<0.001 , respectively ) , improved the WHO functional class ( P=0.003 , P<0.001 , and P<0.001 , respectively ) , and were associated with side effects such as flushing , dyspepsia , and diarrhea . The incidence of clinical worsening did not differ significantly between the patients treated with sildenafil and those treated with placebo . Among the 222 patients completing one year of treatment with sildenafil monotherapy , the improvement from baseline at one year in the distance walked in six minutes was 51 m. CONCLUSIONS Sildenafil improves exercise capacity , WHO functional class , and hemodynamics in patients with symptomatic pulmonary arterial hypertension",
    "BACKGROUND Current therapies for pulmonary arterial hypertension have been adopted on the basis of short-term trials with exercise capacity as the primary end point . We assessed the efficacy of macitentan , a new dual endothelin-receptor antagonist , using a primary end point of morbidity and mortality in a long-term trial . METHODS We r and omly assigned patients with symptomatic pulmonary arterial hypertension to receive placebo once daily , macitentan at a once-daily dose of 3 mg , or macitentan at a once-daily dose of 10 mg . Stable use of oral or inhaled therapy for pulmonary arterial hypertension , other than endothelin-receptor antagonists , was allowed at study entry . The primary end point was the time from the initiation of treatment to the first occurrence of a composite end point of death , atrial septostomy , lung transplantation , initiation of treatment with intravenous or subcutaneous prostanoids , or worsening of pulmonary arterial hypertension . RESULTS A total of 250 patients were r and omly assigned to placebo , 250 to the 3-mg macitentan dose , and 242 to the 10-mg macitentan dose . The primary end point occurred in 46.4 % , 38.0 % , and 31.4 % of the patients in these groups , respectively . The hazard ratio for the 3-mg macitentan dose as compared with placebo was 0.70 ( 97.5 % confidence interval [ CI ] , 0.52 to 0.96 ; P=0.01 ) , and the hazard ratio for the 10-mg macitentan dose as compared with placebo was 0.55 ( 97.5 % CI , 0.39 to 0.76 ; P<0.001 ) . Worsening of pulmonary arterial hypertension was the most frequent primary end-point event . The effect of macitentan on this end point was observed regardless of whether the patient was receiving therapy for pulmonary arterial hypertension at baseline . Adverse events more frequently associated with macitentan than with placebo were headache , nasopharyngitis , and anemia . CONCLUSIONS Macitentan significantly reduced morbidity and mortality among patients with pulmonary arterial hypertension in this event-driven study . ( Funded by Actelion Pharmaceuticals ; SERAPHIN Clinical Trials.gov number , NCT00660179 . )",
    "Our previous studies have shown that bone marrow mesenchymal stem cells ( BMSCs ) can inhibit the progression of pulmonary artery hypertension ( PAH ) in the monocrotaline ( MCT ) model in the short term . The aim of this study was to further investigate the long-term effect of BMSCs on PAH and to explore the mechanism of the protective effect including the pulmonary vascular remodeling and cell differentiation . PAH model was established by subcutaneous injection of 50 mg/kg MCT as previously study . Postoperatively , the animals were r and omly divided into three groups ( n = 10 in each group ) : control , PAH group , and BMSCs implantation group . Six months after injection , immunology and immunohistochemistry analysis indicated the  MCT-induced intima-media thickness in muscular arteries was reduced ( P < 0.05 ) ; the area of collagen fibers in lung tissue was lower ( P < 0.05 ) , and the proliferating cell nuclear antigen level in pulmonary artery smooth muscle cells was decreased ( P < 0.05 ) . Immunofluorescence showed that the cells have the ability to differentiate between von Willebr and factor and vascular endothelial growth factor . Six months after intravenous injection , BMSCs could significantly improve pulmonary function by inhibiting the ventricular remodeling and the effect of cell differentiation",
    "Experimental data suggest that transplantation of EPCs attenuates monocrotaline-induced pulmonary hypertension in rats and dogs . In addition , our previous studies suggested that autologous EPC transplantation was feasible , safe , and might have beneficial effects on exercise capacity and pulmonary hemodynamics in adults with IPAH . Thus , we hypothesized that transplantation of EPCs would improve exercise capacity and pulmonary hemodynamics in children with IPAH . Thirteen children with IPAH received intravenous infusion of autologous EPCs . The right-sided heart catheterization and 6-MWD test were performed at baseline and at the time of 12 wk after cell infusion . At the time of 12 wk , mPAP decreased by 6.4 mmHg from 70.3 + /- 19.0 to 63.9 + /- 19.3 mmHg ( p = 0.015 ) . PVR decreased by approximately 19 % from 1118 + /- 537 to 906 + /- 377 dyn s/cm(5 ) ( p = 0.047 ) . CO increased from 3.39 + /- 0.79 to 3.85 + /- 0.42 L/min ( p = 0.048 ) . The 6-MWD increased by 39 m from 359 + /- 82 to 399 + /- 74 m ( p = 0.012 ) . NYHA functional class also improved . There were no severe adverse events with cell infusion . The small pilot study suggested that intravenous infusion of autologous EPCs was feasible , safe , and associated with significant improvements in exercise capacity , NYHA functional class , and pulmonary hemodynamics in children with IPAH . Confirmation of these results in a r and omized controlled trial are essential",
    "BACKGROUND Uncontrolled studies suggested that aerosolized iloprost , a stable analogue of prostacyclin , causes selective pulmonary vasodilatation and improves hemodynamics and exercise capacity in patients with pulmonary hypertension . METHODS We compared repeated daily inhalations of 2.5 or 5.0 microg of iloprost ( six or nine times per day ; median inhaled dose , 30 microg per day ) with inhalation of placebo .  A total of 203 patients with selected forms of severe pulmonary arterial hypertension and chronic thromboembolic pulmonary hypertension ( New York Heart Association [ NYHA ] functional class III or IV ) were included . The primary end point was met if , after week 12 , the NYHA class and distance walked in six minutes were improved by at least one class and at least 10 percent , respectively , in the absence of clinical deterioration according to predefined criteria and death . RESULTS The combined clinical end point was met by 16.8 percent of the patients receiving iloprost , as compared with 4.9 percent of the patients receiving placebo ( P=0.007 ) . There were increases in the distance walked in six minutes of 36.4 m in the iloprost group as a whole ( P=0.004 ) and of 58.8 m in the subgroup of patients with primary pulmonary hypertension . Overall , 4.0 percent of patients in the iloprost group ( including one who died ) and 13.7 percent of those in the placebo group ( including four who died ) did not complete the study ( P=0.024 ) ; the most common reason for withdrawal was clinical deterioration . As compared with base-line values , hemodynamic values were significantly improved at 12 weeks when measured after iloprost inhalation ( P<0.001 ) , were largely unchanged when measured before iloprost inhalation , and were significantly worse in the placebo group . Further significant beneficial effects of iloprost treatment included an improvement in the NYHA class ( P=0.03 ) , dyspnea ( P=0.015 ) , and quality of life ( P=0.026 ) . Syncope occurred with similar frequency in the two groups but was more frequently rated as serious in the iloprost group , although this adverse effect was not associated with clinical deterioration . CONCLUSIONS Inhaled iloprost is an effective therapy for patients with severe pulmonary hypertension",
    "BACKGROUND High pulmonary vascular resistance ( PVR ) may be a risk factor for early and late mortality in both Glen shunt and Fontan operation patients . Furthermore , PVR may increase long after the Fontan operation . Whether pulmonary vasodilators such as phosphodiesterase 5 inhibitors can decrease PVR in patients with single ventricular physiology remains undetermined . METHODS AND RESULTS This was a prospect i ve , multicenter study . Patients with single ventricular physiology who have a PVR index higher than 2.5 Wood units \\u00b7 \\u33a1 ( WU ) were enrolled .  Cardiac catheterization was performed before and after administration of sildenafil in all patients . After the Fontan operation , a  six minute walk test  ( 6MWT ) was also performed . A total of 42 patients were enrolled . PVR was significantly decreased in each stage of single ventricular physiology after sildenafil administration : from 4.3\\u00b11.5WU to 2.1\\u00b10.6WU ( p<0.01 ) in patients before a Glenn shunt , from 3.2\\u00b10.5WU to 1.6\\u00b10.6WU ( p<0.001 ) in patients after a Glenn shunt , and from 3.9\\u00b11.7WU to 2.3\\u00b10.8WU ( p<0.001 ) in patients after Fontan . In patients after Fontan , the 6MWT increased from 416\\u00b174 m to 485\\u00b172 m ( p<0.01 ) , and NYHA functional class improved significantly ( p<0.05 ) after sildenafil administration . No major side effects were observed in any patients . CONCLUSIONS Sildenafil reduced PVR in patients with single ventricle physiology . Sildenafil increased exercise capacity and improved NYHA functional class in patients after a Fontan operation . This implies that pulmonary vasodilation is a potential therapeutic target in selected patients with elevated PVR with single ventricle physiology . Long-term clinical significance warrants further study",
    "OBJECTIVES The purpose of this study was to examine the efficacy and safety of four doses of ambrisentan , an oral endothelin type A receptor-selective antagonist , in patients with pulmonary arterial hypertension ( PAH ) . BACKGROUND Pulmonary arterial hypertension is a life-threatening and progressive disease with limited treatment options . Endothelin is a vasoconstrictor and smooth muscle cell mitogen that plays a critical role in the pathogenesis and progression of PAH . METHODS In this double-blind , dose-ranging study , 64 patients with idiopathic PAH or PAH associated with collagen vascular disease , anorexigen use , or human immunodeficiency virus infection were r and omized to receive 1 , 2.5 , 5 , or 10 mg of ambrisentan once daily for 12 weeks followed by 12 weeks of open-label ambrisentan . The primary end point was an improvement from baseline in 6-min walk distance ( 6MWD ) ; secondary end points included Borg dyspnea index , World Health Organization ( WHO ) functional class , a subject global assessment , and cardiopulmonary hemodynamics . RESULTS At 12 weeks , ambrisentan increased 6MWD ( + 36.1 m , p < 0.0001 ) with similar and statistically significant increases for each dose group ( range , + 33.9 to + 38.1 m ) . Improvements were also observed in Borg dyspnea index , WHO functional class , subject global assessment , mean pulmonary arterial pressure ( -5.2 mm Hg , p < 0.0001 ) , and cardiac index ( + 0.33 l/min/m2 , p < 0.0008 ) . Adverse events were mild and unrelated to dose , including the incidence of elevated serum aminotransferase concentrations > 3 times the upper limit of normal ( 3.1 % ) . CONCLUSIONS Ambrisentan appears to improve exercise capacity , symptoms , and hemodynamics in patients with PAH . The incidence and severity of liver enzyme abnormalities appear to be low",
    "UNLABELLED Pulmonary arterial hypertension ( PAH ) is characterized by functional and structural changes in the pulmonary vasculature , and despite the drug treatment that made significant progress , the prognosis of patients with advanced PH remains extremely poor . In the present study , we investigated the early effect of bone marrow mesenchymal stem cells ( BMSCs ) on experimental high blood flow-induced PAH model rats and discussed the mechanism . BMSCs were isolated , cultured from bone marrow of Sprague-Dawley ( SD ) rat . The animal model of PAH was created by surgical methods to produce a left-to-right shunt . Following the successful establishment of the PAH model , rats were r and omly assigned to three groups ( n=20 in each group ) : sham group ( control ) , PAH group , and BMSC group ( received a sublingual vein injection of 1 - 5 \\u00d7 10(6 ) BMSCs ) . Two weeks after the administration , BMSCs significantly reduced the vascular remodeling , improved the hemodynamic data , and deceased the right ventricle weight ratio to left ventricular plus septal weight ( RV/LV+S ) ( P<0.05 ) . Real-time reverse transcription-polymerase chain reaction ( RT-PCR ) and immunohistochemistry analysis results indicated that the inflammation factors such as interleukin-1\\u03b2 ( IL-1\\u03b2 ) , IL-6 , and tumor necrosis factor-\\u03b1 ( TNF-\\u03b1 ) were reduced ( P<0.05 ) ; the expression of matrix metallo proteinase-9 ( MMP-9 ) was lower ( P<0.05 ) ; vascular endothelial growth factor ( VEGF ) was higher in BMSC group than those in PAH group ( P<0.05 ) . CONCLUSION Sublingual vein injection of BMSCs for 2 weeks , significantly improved the lung and heart injury caused by left-to-right shunt-induced PAH ; decreased pulmonary vascular remodeling and inflammation ; and enhanced angiogenesis",
    "Pulmonary arterial hypertension is a life-threatening disease for which continuous intravenous prostacyclin has proven to be effective . However , this treatment requires a permanent central venous catheter with the associated risk of serious complications such as sepsis , thromboembolism , or syncope . Treprostinil , a stable prostacyclin analogue , can be administered by a continuous subcutaneous infusion , avoiding these risks . We conducted a 12-week , double-blind , placebo-controlled multicenter trial in 470 patients with pulmonary arterial hypertension , either primary or associated with connective tissue disease or congenital systemic-to-pulmonary shunts .  Exercise capacity improved with treprostinil and was unchanged with placebo ; the between treatment group difference in median six-minute walking distance was 16 m ( p = 0.006 ) . Improvement in exercise capacity was greater in the sicker patients and was dose-related , but independent of disease etiology . Concomitantly , treprostinil significantly improved indices of dyspnea , signs and symptoms of pulmonary hypertension , and hemodynamics . The most common side effect attributed to treprostinil was infusion site pain ( 85 % ) leading to premature discontinuation from the study in 8 % of patients . Three patients in the treprostinil treatment group presented with an episode of gastrointestinal hemorrhage . We conclude that chronic subcutaneous infusion of treprostinil is an effective treatment with an acceptable safety profile in patients with pulmonary arterial hypertension",
    "BACKGROUND Endothelin 1 , a powerful endogenous vasoconstrictor and mitogen , might be a cause of pulmonary hypertension . We describe the efficacy and safety of bosentan , a dual endothelin-receptor antagonist that can be taken orally , in patients with severe pulmonary hypertension . METHODS In this double-blind , placebo-controlled study , 32 patients with pulmonary hypertension ( primary or associated with scleroderma ) were r and omly assigned to bosentan ( 62.5 mg taken twice daily for 4 weeks then 125 mg twice daily ) or placebo for a minimum of 12 weeks . The primary endpoint was change in exercise capacity . Secondary endpoints included changes in cardiopulmonary haemodynamics , Borg dyspnoea index , WHO functional class , and withdrawal due to clinical worsening . Analysis was by intention to treat . FINDINGS In patients given bosentan , the distance walked in 6 min improved by 70 m at 12 weeks compared with baseline , whereas it worsened by 6 m in those on placebo ( difference 76 m [ 95 % CI 12 - 139 ] , p=0.021 ) . The improvement was maintained for at least 20 weeks . The cardiac index was 1.0 L min(-1 ) m(-2 ) ( 95 % CI 0.6 - 1.4 , p<0.0001 ) greater in patients given bosentan than in those given placebo .  Pulmonary vascular resistance decreased by 223 dyn s cm(-)(5 ) with bosentan , but increased by 191 dyn s cm(-5 ) with placebo ( difference -415 [ -608 to -221 ] , p=0.0002 ) . Patients given bosentan had a reduced Borg dyspnoea index and an improved WHO functional class . All three withdrawals from clinical worsening were in the placebo group ( p=0.033 ) . The number and nature of adverse events did not differ between the two groups . INTERPRETATION Bosentan increases exercise capacity and improves haemodynamics in patients with pulmonary hypertension , suggesting that endothelin has an important role in pulmonary hypertension",
    "Background Systematic Review s ( SRs ) of experimental animal studies are not yet common practice , but awareness of the merits of conducting such SRs is steadily increasing . As animal intervention studies differ from r and omized clinical trials ( RCT ) in many aspects , the methodology for SRs of clinical trials needs to be adapted and optimized for animal intervention studies . The Cochrane Collaboration developed a Risk of Bias ( RoB ) tool to establish consistency and avoid discrepancies in assessing the method ological quality of RCTs . A similar initiative is warranted in the field of animal experimentation . Methods We provide an RoB tool for animal intervention studies ( SYRCLE \\u2019s RoB tool ) . This tool is based on the Cochrane RoB tool and has been adjusted for aspects of bias that play a specific role in animal intervention studies . To enhance transparency and applicability , we formulated signalling questions to facilitate judgment . Results The result ing RoB tool  for animal studies contains 10 entries . These entries are related to selection bias , performance bias , detection bias , attrition bias , reporting bias and other biases . Half these items are in agreement with the items in the Cochrane RoB tool . Most of the variations between the two tools are due to differences in design between RCTs and animal studies . Shortcomings in , or unfamiliarity with , specific aspects of experimental design of animal studies compared to clinical studies also play a role . Conclusions SYRCLE \\u2019s RoB tool is an adapted version of the Cochrane RoB tool . Widespread adoption and implementation of this tool will facilitate and improve critical appraisal of evidence from animal studies . This may subsequently enhance the efficiency of translating animal research into clinical practice and increase awareness of the necessity of improving the method ological quality of animal studies"
  ],
  "target": "Conclusions SC therapy is effective for PAH in pre clinical studies .\\nThese results may help to st and ardise pre clinical animal studies and provide a theoretical basis for clinical trial design in the future .",
  "background": "Background Despite significant progress in drug treatment , the prognosis of patients with advanced pulmonary arterial hypertension ( PAH ) remains extremely poor .\\nMany pre clinical studies have reported the efficacy of stem cell ( SC ) therapy for PAH ; however , this approach remains controversial .\\nThe aim of this systematic review and meta- analysis is to assess the potential efficacy of SC therapy for PAH .",
  "reviews_info": "Background Despite significant progress in drug treatment , the prognosis of patients with advanced pulmonary arterial hypertension ( PAH ) remains extremely poor .\\nMany pre clinical studies have reported the efficacy of stem cell ( SC ) therapy for PAH ; however , this approach remains controversial .\\nThe aim of this systematic review and meta- analysis is to assess the potential efficacy of SC therapy for PAH ."
}
```



__Cochrane__

```json
{
  "review_id": "CD007697",
  "pmid": [
    "16394043"
  ],
  "title": [
    "Aggressive surgical effort and improved survival in advanced-stage ovarian cancer."
  ],
  "abstract": [
    "Residual disease after initial surgery for ovarian cancer is the strongest prognostic factor for survival. However, the extent of surgical resection required to achieve optimal cytoreduction is controversial. Our goal was to estimate the effect of aggressive surgical resection on ovarian cancer patient survival.\\n                A retrospective cohort study of consecutive patients with International Federation of Gynecology and Obstetrics stage IIIC ovarian cancer undergoing primary surgery was conducted between January 1, 1994, and December 31, 1998. The main outcome measures were residual disease after cytoreduction, frequency of radical surgical resection, and 5-year disease-specific survival.\\n                The study comprised 194 patients, including 144 with carcinomatosis. The mean patient age and follow-up time were 64.4 and 3.5 years, respectively. After surgery, 131 (67.5%) of the 194 patients had less than 1 cm of residual disease (definition of optimal cytoreduction). Considering all patients, residual disease was the only independent predictor of survival; the need to perform radical procedures to achieve optimal cytoreduction was not associated with a decrease in survival. For the subgroup of patients with carcinomatosis, residual disease and the performance of radical surgical procedures were the only independent predictors. Disease-specific survival was markedly improved for patients with carcinomatosis operated on by surgeons who most frequently used radical procedures compared with those least likely to use radical procedures (44% versus 17%, P < .001).\\n                Overall, residual disease was the only independent predictor of survival. Minimizing residual disease through aggressive surgical resection was beneficial, especially in patients with carcinomatosis.\\n                II-2."
  ],
  "target": "We found only low quality evidence comparing ultra-radical and standard surgery in women with advanced ovarian cancer and carcinomatosis. The evidence suggested that ultra-radical surgery may result in better survival.\\u00a0 It was unclear whether there were any differences in progression-free survival, QoL and morbidity between the two groups. The cost-effectiveness of this intervention has not been investigated. We are, therefore, unable to reach definite conclusions about the relative benefits and adverse effects of the two types of surgery.\\nIn order to determine the role of ultra-radical surgery in the management of advanced stage ovarian cancer, a sufficiently powered randomised controlled trial comparing ultra-radical and standard surgery or well-designed non-randomised studies would be required."
}
```

### Data Fields

[Needs More Information]

### Data Splits

Each dataset is split into training, validation and test partitions

__MS^2__

| train | validation | test |
|------:|-----------:|-----:|
| 14188 |       2021 | 1667 |

__Cochrane__

| train | validation | test |
|------:|-----------:|-----:|
|  3752 |        470 |  470 |


## Dataset Creation

Please refer to the following papers for details about dataset curation:

[MSˆ2: A Dataset for Multi-Document Summarization of Medical Studies](https://aclanthology.org/2021.emnlp-main.594.pdf)

[Generating (Factual?) Narrative Summaries of RCTs: Experiments with Neural Multi-Document Summarization](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8378607/)

### Curation Rationale

[Needs More Information]

### Source Data

#### Initial Data Collection and Normalization

[Needs More Information]

#### Who are the source language producers?

[Needs More Information]

### Annotations

#### Annotation process

[Needs More Information]

#### Who are the annotators?

[Needs More Information]

### Personal and Sensitive Information

[Needs More Information]

## Considerations for Using the Data

### Social Impact of Dataset

[Needs More Information]

### Discussion of Biases

[Needs More Information]

### Other Known Limitations

[Needs More Information]

## Additional Information

### Dataset Curators

[Needs More Information]

### Licensing Information

Licensing information can be found [here](https://github.com/allenai/mslr-shared-task/blob/main/LICENSE).

### Citation Information

**DeYoung, Jay, Iz Beltagy, Madeleine van Zuylen, Bailey Kuehl and Lucy Lu Wang. "MS2: A Dataset for Multi-Document Summarization of Medical Studies." EMNLP (2021).**

```bibtex
@inproceedings{DeYoung2021MS2MS,
  title={MSˆ2: Multi-Document Summarization of Medical Studies},
  author={Jay DeYoung and Iz Beltagy and Madeleine van Zuylen and Bailey Kuehl and Lucy Lu Wang},
  booktitle={EMNLP},
  year={2021}
}
```

**Byron C. Wallace, Sayantani Saha, Frank Soboczenski, and Iain James Marshall. (2020). "Generating (factual?) narrative summaries of RCTs: Experiments with neural multi-document summarization." AMIA Annual Symposium.**

```bibtex
@article{Wallace2020GeneratingN,
  title={Generating (Factual?) Narrative Summaries of RCTs: Experiments with Neural Multi-Document Summarization},
  author={Byron C. Wallace and Sayantani Saha and Frank Soboczenski and Iain James Marshall},
  journal={AMIA Annual Symposium},
  year={2020},
  volume={abs/2008.11293}
}
```