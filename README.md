# ABUSE AI

ABUSE AI is a prototype API that uses machine learning
techniques to classify complaints and extract offending IPs.  

The type field returns a JS object containing the confidence level of 
prediction for each type of complaint.  For example: a .95 confidence
level for malicious content means the model is 95% sure the sent
text was from a malicious content complaint.

The project is currently a prototype & the base data set's label accuracy is 
questionable. The text classification process in place is also rudimentary.
Therefore, event though the API can classify emails successfully in the wild,
use it in production at your own risk.

Live version at: http://abuseai.us-east-1.elasticbeanstalk.com/

## Contributing 

Due to the sensitive nature of the data involved. If you wish to contribue, 
please open an issue requesting the data and a description of your intention.
I will provide you with the necessary data set upon receipt.

With more data more distinct classification would be possible. If you wish
to provide additional data, please open an issue as well.

## Usage

To use the api POST a `subject` and `body` to `www.AbuseAI.com/api/email`.

`curl --data "subject=Phishing attack&body=Phising attack from site emulating bank at ip 8.8.4.4" http://abuseai.us-east-1.elasticbeanstalk.com/api/email`

## Prediction Classes

There are currently 3 prediction classes that encompass a variety of 
complaints. 

### Malicious Content

Any complaint relating to websites which are serving malicious content such
as malware, fraudulate sites, phishing, pedophilia, or other criminal
activity.

### Malicious Activity

Any complaint about servers performing brute force attacks, DDOS, portscans,
intrusions and other network attacks as well as playstation abuse, pharming,
spam, and other malicious activity.

### Trademark Infringement

Any complaint pertaining to copyright, trademark, or intellectual property
infringment as well as DMCA take down notices.


## Deployment

1. `git archive -v -o api-$(git rev-parse --short HEAD).zip --format=zip HEAD --worktree-attributes`.
2. Upload a new version in the ElasticBeanstalk console. 
