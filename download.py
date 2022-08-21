import os

try:
    from requests_html import HTMLSession
except ImportError:
    HTMLSession = None

try:
    import wget
except ImportError:
    wget = None

if not HTMLSession:
    print('Please run "pip install requests_html" first')
    exit(1)

if not wget:
    print('Please run "pip install wget" first')
    exit(1)

### 6.21 PM oral paper
Segmentation_Oral_list =[
    'CMT-DeepLab Clustering Mask Transformers for Panoptic Segmentation',
    'Unsupervised Hierarchical Semantic Segmentation With Multiview Cosegmentation and Clustering Transformers',
    'Rethinking Semantic Segmentation A Prototype View',
    'Semantic-Aware Domain Generalized Segmentation',
    'Adaptive Early-Learning Correction for Segmentation From Noisy Annotations',
    'Pointly-Supervised Instance Segmentation',
    'Joint Forecasting of Panoptic Segmentations With Difference Attention',
    'FocusCut Diving Into a Focus View in Interactive Segmentation',
    'Human Instance Matting via Mutual Guidance and Multi-Instance Refinement',
    'Deformable Sprites for Unsupervised Video Decomposition',
    'Eigencontours Novel Contour Descriptors Based on Low-Rank Approximation',
    'Robust and Accurate Superquadric Recovery A Probabilistic Approach',
    'Medial Spectral Coordinates for 3D Shape Analysis',
    'Scribble-Supervised LiDAR Semantic Segmentation',
    'SoftGroup for 3D Instance Segmentation on Point Clouds',
]
Segmentation_Oral_list = [s.replace(' ','_') for s in Segmentation_Oral_list]

Three_D_Oral_list = [
    'Accurate 3D Body Shape Regression Using Metric and Semantic Attributes',
    'JIFF Jointly-Aligned Implicit Face Function for High Quality Single View Clothed Human Reconstruction',
    'Tracking People by Predicting 3D Appearance, Location and Pose',
    'ArtiBoost Boosting Articulated 3D Hand-Object Pose Estimation via Online Exploration and Synthesis',
    'Interacting Attention Graph for Single Image Two-Hand Reconstruction',
    '3D Human Tongue Reconstruction From Single In-the-Wild Images',
    'EPro-PnP Generalized End-to-End Probabilistic Perspective-N-Points for Monocular Object Pose Estimation',
    'Diversity Matters Fully Exploiting Depth Clues for Reliable Monocular 3D Object Detection',
    'OmniFusion 360 Monocular Depth Estimation via Geometry-Aware Fusion',
    'Gated2Gated Self-Supervised Depth Estimation From Gated Images',
    'IRISformer Dense Vision Transformers for Single-Image Inverse Rendering in Indoor Scenes',
    'Egocentric Scene Understanding via Multimodal Spatial Rectifier',
    'Multi-View Depth Estimation by Fusing Single-View Depth Probability With Multi-View Geometry',
    'The Implicit Values of a Good Hand Shake: Handheld Multi-Frame Neural Depth Refinement',
    'BANMo Building Animatable 3D Neural Models From Many Casual Videos',
]

Three_D_Oral_list = [s.replace(' ','_') for s in Three_D_Oral_list]


Video_Oral_list = [
    'Self-Supervised Video Transformer',
    'Temporally Efficient Vision Transformer for Video Instance Segmentation',
    'VISOLO Grid-Based Space-Time Aggregation for Efficient Online Video Instance Segmentation',
    'Temporal Alignment Networks for Long-Term Video',
    'Revisiting the Video in Video-Language Understanding',
    'Invariant Grounding for Video Question Answering',
    'P3IV: Probabilistic Procedure Planning From Instructional Videos With Weak Supervision',
    'FineDiving A Fine-Grained Dataset for Procedure-Aware Action Quality Assessment',
    'Cross-Model Pseudo-Labeling for Semi-Supervised Action Recognition',
    'Revisiting Skeleton-Based Action Recognition',
    'OpenTAL Towards Open Set Temporal Action Localization',
    'Dual-AI Dual-Path Actor Interaction Learning for Group Activity Recognition',
    'TransRank Self-Supervised Video Representation Learning via Ranking-Based Transformation Recognition',
    'Revealing Occlusions With 4D Neural Fields',
    'HODOR High-Level Object Descriptors for Object Re-Segmentation in Video Learned From Static Images'
]

Video_Oral_list = [s.replace(' ','_') for s in Video_Oral_list]


#### 6.22 AM
Recognition_Oral_list = [

]

####################################################

def Is_oral(name,paper_list):
    for paper in paper_list:
        if len(paper) > 80:
            paper = paper[:50]
        if paper in name:
            return True
    return False


def main(pdf_links, folder,paper_list):
    '''
    url: link,
    foler: folder name,
    paper_list: the title of papers that we want.
    '''
    total = len(paper_list)
    # check dir
    if not os.path.exists(folder):
        os.mkdir(folder)
        
    if len(os.listdir(folder)) == total:
        print('All papers exist!')
        return
        
    count = 0
    for idx, link in enumerate(pdf_links, start=1):
        name = link[link.rindex('/') + 1:]
        filename = os.path.join(folder, name)
        ### 跳过supplemental，
        if 'supplemental' in filename:
            continue
        if Is_oral(name,paper_list):
            if os.path.exists(filename):
                print(name,' exists!')
                continue
            # save file
            count += 1
            print('Downloading {} / {} : {}'.format(count, total, name))
            wget.download(link, filename)
            print('\n')
    print('Finish')
    print('There are {}/{} papers in {}'.format(len(os.listdir(folder)),total,folder))
    


def get_session(url):
    sess = HTMLSession()
    r = sess.get(url)
    ### get session title
    session_titles = []
    
    for t in r.html.find('h4'):
        if t.text:
            start = [substr.end() for substr in re.finditer('Session Title:',t.text)][0]
            end =  [substr.end() for substr in re.finditer('\n',t.text)][-1]
            title = t.text[start:end]
            title = title.replace(':','')
            title = title.replace(',',' ')
            title = title.replace('!',' ')
            title = title.replace('\n','')
            title = title.replace('\xa0','')
            title = title.replace('/','')
            session_titles.append(title)
    
    sess.close()
    print(session_titles)
    return session_titles


if __name__ == '__main__':
    import pandas as pd
    import re
    import pdb
    
    url = r'https://cvpr2022.thecvf.com/orals-622-am'
    sess = HTMLSession()
    r = sess.get(url)
    # get all oral links
    all_absolute_links = r.html.absolute_links
    oral_link_list = list(filter(lambda x: 'orals' in x, all_absolute_links))
    sess.close()
    ### cvpr pdf links
    url = r'https://openaccess.thecvf.com/CVPR2022?day=all'
    sess = HTMLSession()
    r = sess.get(url)
    # get all absolute links
    all_absolute_links = r.html.absolute_links
    # filter .pdf links
    pdf_links = list(filter(lambda x: x.endswith('.pdf'), all_absolute_links))
    
    for oral_link in oral_link_list:
        print('oral link: ', oral_link)
        oral_name = oral_link[oral_link.rindex('/') + 1:]
        ## get session title
        session_titles = get_session(oral_link)
        ## get paper title
        df = pd.read_html(oral_link)
        for idx,filename in enumerate(session_titles):
            if '622' in oral_name and idx == 2:
                paper_list = [s.replace(':','') for s in df[idx][-2][1:] if isinstance(s,str)]
            else:
                paper_list = [s.replace(':','') for s in df[idx][-2][1:] if isinstance(s,str)]
            paper_list = [s.replace(' ','_') for s in paper_list]
            dir = os.path.join(oral_name,filename)
            print('Session: ',filename,' There are ', len(paper_list),' papers in all!')
            main(pdf_links,dir,paper_list)
        print('==='*20)
    sess.close()
    exit()
    ###### 6.21 AM
    url = r'https://openaccess.thecvf.com/CVPR2022?day=2022-06-21'
    ### Session Title: Segmentation, Grouping and Shape Analysis
    filename = './Segmentation, Grouping and Shape Analysis'
    print('6.21 AM oral paper about Segmentation, Grouping and Shape Analysis! There are ',len(Segmentation_Oral_list), 'papers in all!'  )
#    main(url, filename,Segmentation_Oral_list)
    
    ### Session Title: 3D From Single Images
    filename = './3D From Single Images'
    print('6.21 AM oral paper about 3D From Single Images! There are ',len(Three_D_Oral_list), 'papers in all!'  )
    main(url, filename,Three_D_Oral_list)
    
    ### Session Title: Video Analysis & Understanding
    filename = './Video Analysis & Understanding'
    print('6.21 AM oral paper about Video Analysis & Understanding! There are ',len(Video_Oral_list), 'papers in all!'  )
    main(url, filename,Video_Oral_list)
    
    
    #### 6.22 AM
    filename ='./Recognition-Detection, Categorization, Retrieval'
    print('6.21 AM oral paper about Recognition: Detection, Categorization, Retrieval! There are ',len(Recognition_Oral_list), 'papers in all!'  )
    main(url, filename,Recognition_Oral_list)
