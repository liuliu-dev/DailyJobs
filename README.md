# DailyJobs
Collecting job listings information from LinkedIn

<h2>Example usage</h2>

```
#use your LinkedIn account and password to login 
email = "YourAccount"
password = "Password"

#run login and return driver
wd=LinkedInLogin().run(email,password)

#use your own job search link, here we have software engineer job search in the U.S. for example 
url='https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=United%20States&locationId=&geoId=103644278&sortBy=R&f_TPR=r86400&position=1&pageNum=0'
wd.get(url)
```

<h2>Terms and Conditions</h2>
By using this project, you agree to the following Terms and Conditions. We reserve the right to block any user of this repository that does not meet these conditions.

<h2>Usage</h2>
This project may not be used for any of the following:
<ul>
<li>Commercial use</li>
<li>Spam</li>
<li>Storage of any Personally Identifiable Information</li>
<li>Personal abuse (i.e. verbal abuse)</li>
</ul>

<h2>Legal</h2>
This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by Linkedin or any of its affiliates or subsidiaries. This is an independent and unofficial API. Use at your own risk.
