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


####################################################

def Is_oral(name, paper_list):
    for paper in paper_list:
        if len(paper) > 80:
            paper = paper[:50]
        if paper in name:
            return True
    return False


def main(pdf_links, folder, paper_list):
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
        if Is_oral(name, paper_list):
            if os.path.exists(filename):
                print(name, ' exists!')
                continue
            # save file
            count += 1
            print('Downloading {} / {} : {}'.format(count, total, name))
            wget.download(link, filename)
            print('\n')
    print('Finish')
    print('There are {}/{} papers in {}'.format(len(os.listdir(folder)), total, folder))


def get_session(url):
    sess = HTMLSession()
    r = sess.get(url)
    ### get session title
    session_titles = []
    for t in r.html.find('h4'):
        if t.text:
            start = [substr.end() for substr in re.finditer('Session Title:', t.text)][0]
            end = [substr.end() for substr in re.finditer('\n', t.text)][-1]
            title = t.text[start:end]
            title = title.replace(':', '')
            title = title.replace(',', ' ')
            title = title.replace('!', ' ')
            title = title.replace('\n', '')
            title = title.replace('\xa0', '')
            title = title.replace('/', '')
            session_titles.append(title)

    sess.close()
    print('session_titles: ', session_titles)
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
        ## mkdir
        if not os.path.exists(oral_name):
            os.mkdir(oral_name)

        ## get session title
        session_titles = get_session(oral_link)
        ## get paper title
        df = pd.read_html(oral_link)
        for idx, filename in enumerate(session_titles):
            if '622' in oral_name and idx == 2:
                paper_list = [s.replace(':', '') for s in df[idx][3][1:] if isinstance(s, str)]
            else:
                paper_list = [s.replace(':', '') for s in df[idx][1][1:] if isinstance(s, str)]
            paper_list = [s.replace(' ', '_') for s in paper_list]
            dir = os.path.join(oral_name, filename)
            print('Session: ', filename, '.There are ',len(paper_list),' papers in all!')
            main(pdf_links, dir, paper_list)
        print('===' * 20)
    sess.close()

