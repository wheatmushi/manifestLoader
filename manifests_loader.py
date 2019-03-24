# load flight manifests by date

import auth
import os
import json

os.environ['url_main'] = 'https://admin-su.crewplatform.aero/'
url_main = os.environ.get('url_main')

start_date = '28/Jan/2019'
end_date = '30/Jan/2019'

url_manifest = os.environ['url_main'] + 'core/monitoring/ajax/manifests?draw=4&columns[0][data]=id&columns[0][name]=id&columns[0][searchable]=false&columns[0][orderable]=true&columns[0][search][value]=&columns[0][search][regex]=false&columns[1][data]=filename&columns[1][name]=filename&columns[1][searchable]=true&columns[1][orderable]=true&columns[1][search][value]=&columns[1][search][regex]=false&columns[2][data]=type&columns[2][name]=type&columns[2][searchable]=true&columns[2][orderable]=true&columns[2][search][value]=&columns[2][search][regex]=false&columns[3][data]=status&columns[3][name]=status&columns[3][searchable]=true&columns[3][orderable]=true&columns[3][search][value]=&columns[3][search][regex]=false&columns[4][data]=inserted&columns[4][name]=inserted&columns[4][searchable]=true&columns[4][orderable]=true&columns[4][search][value]={}%23{}'
url_manifest_filtered = url_manifest.format(start_date, end_date)
url_manifest_download = os.environ['url_main'] + 'core/monitoring/manifest/download/'

session = auth.authentication()[0]

manifests = session.get(url_manifest_filtered)
manifests = json.loads(manifests.content)
print('from ' + str(manifests['recordsTotal']) + ' filtered ' + str(manifests['recordsFiltered']) + ' records')
ids = [(row['id'], row['filename']) for row in manifests['data']]

path = 'manifests_{start}_to_{end}'.format(start=start_date.replace('/',''), end=end_date.replace('/',''))
if not os.path.exists(path):
    os.makedirs(path)

for iteration, filename in enumerate(ids):
    if iteration % 50 == 0 and iteration > 0:
        print(str(iteration) + ' files downloaded')
    file = session.get(url_manifest_download + filename[0], allow_redirects=True)
    with open(os.path.join(path, filename[1]), 'wb') as f:
        f.write(file.content)
