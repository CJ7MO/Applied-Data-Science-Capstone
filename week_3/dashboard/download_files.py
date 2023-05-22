import urllib.request

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
filename = "spacex_dash_app.py"
url1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
filename1 = "spacex_launch_dash.csv"
urllib.request.urlretrieve(url, filename)
urllib.request.urlretrieve(url1, filename1)