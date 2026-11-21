"""Build the short portfolio report from the notebook's aggregate exports.

Run from the repository root after executing the notebook:
    python -m pip install -r reports/requirements.txt
    python reports/build_report.py
"""
from pathlib import Path
import csv
import json
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.graphics import renderSVG

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'results'
summary = json.loads((R / 'run_summary.json').read_text())
def read(name):
    with (R / name).open() as f:
        return list(csv.DictReader(f))
models = read('model_comparison.csv')
controlled = read('input_algorithm_comparison.csv')
review = read('review_capacity.csv')
bootstrap = read('bootstrap.csv')
INK = colors.HexColor('#172D3B')
TEAL = colors.HexColor('#246B70')
MUTED = colors.HexColor('#526675')
PAPER = colors.HexColor('#F0F5F5')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleX',fontName='Helvetica-Bold',fontSize=28,leading=32,textColor=INK,spaceAfter=16))
styles.add(ParagraphStyle(name='Deck',fontName='Helvetica',fontSize=12,leading=18,textColor=MUTED,spaceAfter=15))
styles.add(ParagraphStyle(name='TextX',fontName='Helvetica',fontSize=10,leading=15,textColor=INK,spaceAfter=10))
styles.add(ParagraphStyle(name='SmallX',fontName='Helvetica',fontSize=8,leading=11,textColor=MUTED,spaceAfter=9))
styles.add(ParagraphStyle(name='HeadX',fontName='Helvetica-Bold',fontSize=15,leading=19,textColor=TEAL,spaceBefore=12,spaceAfter=10))
styles.add(ParagraphStyle(name='KickerX',fontName='Helvetica-Bold',fontSize=9,leading=13,textColor=TEAL,spaceAfter=12))
story=[]
def p(text,kind='TextX'):story.append(Paragraph(text,styles[kind]))
def table(rows,widths):
    cooked=[[Paragraph(str(v),styles['SmallX' if i else 'TextX']) for v in row] for i,row in enumerate(rows)]
    t=Table(cooked,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PAPER),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,0),.6,TEAL),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#D8E2E4'))]))
    story.append(t);story.append(Spacer(1,12))

p('PERSONAL PORTFOLIO / HISTORICAL PREDICTION','KickerX')
p('Predicting Kickstarter<br/>campaign success','TitleX')
p('Wanyu (Julia) Chen<br/>Evidence from 331,675 completed campaigns','Deck')
p('Question','HeadX')
p('How well do campaign attributes associated with launch rank eventual success, and how much improvement comes from richer inputs rather than model complexity?')
p('Headline results','HeadX')
table([['Historical test ROC-AUC','Accuracy','Majority baseline'],[f"{summary['roc_auc']:.3f}",f"{summary['accuracy']:.1%}",'59.6% accuracy']],[170,162,167])
p('Selected model: XGBoost with sub-category and title-length features, chosen by five-fold training-sample cross-validation. The common random test sample contains 66,335 campaigns.')
selected_names=['Majority-class benchmark','Logistic: original inputs','Tuned Random Forest','Logistic: expanded inputs','Selected XGBoost with expanded inputs']
labels=['Always predict failure','Logistic regression / baseline inputs','Tuned Random Forest / baseline inputs','Logistic regression / expanded inputs','Selected XGBoost / expanded inputs']
rows=[['Model and input set','Accuracy','ROC-AUC']]
for key,label in zip(selected_names,labels):
    row=next(x for x in models if x['Model']==key)
    rows.append([label,f"{float(row['Accuracy']):.1%}",f"{float(row['ROC_AUC']):.3f}"])
table(rows,[329,85,85])
p('Interpretation','HeadX')
p('Campaign attributes provide useful historical ranking information, but many individual outcomes remain uncertain. The intended use is further evaluation of a review-priority score, not automatic approval or rejection.')
p('Scope: retrospective analysis. Exchange-rate timing and revisions to campaign attributes are not verified; earlier development also reused the random test split. These are not claims of production-ready, point-in-time performance.','SmallX')
story.append(PageBreak())
p('01 / WHAT DRIVES THE RESULT','KickerX')
p('Information and algorithms','TitleX')
p('Compare the same learners across two input sets before attributing a gain to model complexity.','Deck')
rows=[['Algorithm','Baseline CV AUC','Expanded CV AUC']]
for alg in ['Logistic regression','Tuned Random Forest','XGBoost depth 8']:
    a=next(x for x in controlled if x['Algorithm']==alg and x['Input set']=='original inputs')
    b=next(x for x in controlled if x['Algorithm']==alg and x['Input set']=='expanded inputs')
    rows.append([alg,f"{float(a['CV ROC_AUC']):.4f}",f"{float(b['CV ROC_AUC']):.4f}"])
table(rows,[259,120,120])
p('Baseline inputs: main category, log USD goal, duration, country, currency, launch year and month. Expanded inputs add sub-category and title character/word counts. Both richer inputs and model flexibility improve ranking in these common training folds.')
p('Calibration and uncertainty','HeadX')
p(f"The selected model's historical test Brier score is <b>{summary['brier_score']:.4f}</b> (lower is better). The notebook compares predicted probabilities with observed success rates in ten bins. Calibration in future cohorts has not been tested.")
b=bootstrap[0]
p(f"A paired test-sample bootstrap gives a conditional ROC-AUC interval of <b>{float(b['95% interval lower']):.3f}-{float(b['95% interval upper']):.3f}</b>. Fitted predictions are held fixed; this does not include retraining or model-selection uncertainty.")
p('Risk concentration is not intervention benefit','HeadX')
rows=[['Hypothetical review capacity','Failure rate in selected group','Share of all failures reached']]
for x in review:
    rows.append([x['Coach the riskiest'],f"{float(x['Failure rate among coached']):.1%}",f"{float(x['Share of all failures reached']):.1%}"])
table(rows,[166,167,166])
p('These groups were selected retrospectively by predicted risk; no coaching intervention was delivered or evaluated. Campaigns most likely to fail are not necessarily those most likely to benefit from support. A randomized pilot within risk bands would be needed to test that decision.')
story.append(PageBreak())
p('02 / DESIGN, LIMITS, REPRODUCTION','KickerX')
p('What the evidence supports','TitleX')
p('Data and validation','HeadX')
p('Source: Kickstarter Projects by Mickaël Mouillé (Kaggle), file ks-projects-201801.csv. Of 378,661 records, 331,675 are marked successful or failed. Canceled and unfinished campaigns are excluded from the primary outcome. Pledged amounts and backer counts are excluded from predictors.')
p(f"The temporal robustness exercise trains through 2016 and evaluates 2017: ROC-AUC <b>{summary['temporal_2017_auc']:.3f}</b>, versus <b>{summary['random_no_year_auc']:.3f}</b> for the random split with the same no-year input set. Because specification development used observations including 2017, this is not an untouched forecast.")
p('Limits to keep in view','HeadX')
for text in [
'The snapshot does not verify launch-time FX conversion or unchanged campaign titles/categories. Results are retrospective.',
'Early model results were examined on the random test split. Final CV selection does not erase that development reuse.',
'Forest tuning and candidate comparison reuse training folds. These are non-nested selection scores.',
'The historical dummy vocabulary uses the full feature table, without outcomes. Production preprocessing should be learned inside training data.',
'Bootstrap intervals hold fitted models fixed. Ablation and gain importance describe predictive contribution, not causality.',
'The data do not capture creator history, campaign media or marketing reach; current-platform performance is unknown.'
]:p('- '+text)
p('Reproduce and inspect','HeadX')
p('The repository provides one executed notebook, pinned analysis dependencies, aggregate CSV exports, and a run summary with the input checksum and package versions. Raw campaign data are not redistributed. Follow README.md and data/README.md; run this report builder after executing the notebook.')
p('Authorship and provenance','HeadX')
p('Wanyu (Julia) Chen independently completed the data preparation, modelling, validation, interpretation and original deliverables. Developed as part of Business Analytics Using Python at HEC Paris. This portfolio edition is an analysis project, not a peer-reviewed publication or deployed system.')
p('Source: https://www.kaggle.com/datasets/kemical/kickstarter-projects<br/>Repository: https://github.com/juliawychen-sudo/kickstarter-prelaunch-analysis','SmallX')
def footer(canvas,doc):
    canvas.setStrokeColor(colors.HexColor('#D8E2E4'));canvas.line(48,43,547,43)
    canvas.setFont('Helvetica',8);canvas.setFillColor(MUTED)
    canvas.drawString(48,29,'WANYU CHEN  /  KICKSTARTER PRE-LAUNCH ANALYSIS')
    canvas.drawRightString(547,29,str(doc.page))
SimpleDocTemplate(str(ROOT/'reports/project_brief.pdf'),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=57,title='Predicting Kickstarter Campaign Success',author='Wanyu (Julia) Chen').build(story,onFirstPage=footer,onLaterPages=footer)
print('Built reports/project_brief.pdf')
