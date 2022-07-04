from plotly.graph_objs import bar
from plotly import offline 
import requests

#This is the API which contains the top stories of the day 
url = "https://hacker-news.firebaseio.com/v0/topstories.json" 
r = requests.get(url)
print(r.status_code)

#We get a list of post_ids whose info we will store in a list 
r_obj = r.json()
submissions =[]

#Using the loop we store the info we need 
for post_id in r_obj[:10]:
	url = f"https://hacker-news.firebaseio.com/v0/item/{post_id}.json"
	r=requests.get(url)
	print(f"{post_id}'s status_code is: {r.status_code}")
	try:
		r_dict = r.json()
		submission_dict = {
			'descendants':r_dict['descendants'],
			'title':r_dict['title'],
			'link':f"http://news.ycombinator.com/item?id={post_id}"
		}
		submissions.append(submission_dict)
	except KeyError:
		print("Key Error at",post_id)

#We get the bar graph parameters from here
labels = []
scores = []
hovertext = []
for submission in submissions:
	#Plotly can take a link with the same format as HTML
 	labels.append(f"<a href='{submission['link']}'> {submission['title']} </a>")
 	scores.append(submission['descendants'])
 	hovertext.append(submission['title'])

#Data and Layout parameters for plotting 
data = [{
'type':'bar',
'x':labels,
'y':scores,
'hovertext':hovertext,
'marker': {
 'color': 'rgb(233,114,77)',
 'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
 },
'opacity': 0.6,
}]
my_layout = {
	'title':'Most Commented Top Hacker-News Posts',
	'xaxis':{'title':'titles','tickwidth':10},
	'yaxis':{'title':'Comments','tickwidth':10},

}

fig = {'data':data,'layout':my_layout}
offline.plot(fig,filename="data/hacker-news.html")