Gmail	moovv fit <fitmoovv@gmail.com>
iOS App - v1.0.4 - Review comments from Apple and our action items
5 messages
Prafulla Joshi (Patheya) <prafulla@patheya.tech>	Sat, Aug 29, 2026 at 8:46 AM
To: Pawan Deshmukh <pawan.deshmukh@gmail.com>, moovv fit <fitmoovv@gmail.com>, "Shantanu Choudhary (Patheya)" <shantanu@patheya.tech>, "Devang Shirode (Patheya)" <devang@patheya.tech>, "Sudhanshu Kulkarni (Patheya)" <Sudhanshu@patheya.tech>, rahul jain <u2mailrahul@gmail.com>, "ujwal.parker@gmail.com" <ujwal.parker@gmail.com>, "Kundan Chaudhari (Patheya)" <kundan@patheya.tech>
Hi Team,
There are 3 remarks from App about our recent iOS version, I have listed those down here along with details and the ownership.

1. Guideline 2.1(b) - Performance - App Completeness 


Issue Description:
The In-App Purchase products in the app exhibited one or more bugs which create a poor user experience. Specifically, we were unable to complete the in-app purchase. An error message displayed during the process. Review the details and resources below to troubleshoot this issue.

Next Steps:   Apple reviews In-App Purchase products in the sandbox and the In-App Purchase products do not need prior approval to function in review.

Owner: Shantanu and Prafulla

2. Guideline 1.4.1 - Safety - Physical Harm

Issue Description: The app includes medical information but does not include citations for the medical information. 
Specifically, the app provides health or medical recommendations in the app without citations, such as links to sources for this information.
All apps with medical and health information should include citations to ensure users are provided accurate information.

Next Steps: Include citations in the app of the sources of the recommendations or information, such as links to those sources. The citations to the sources should be easy for the user to find.

Owner: Pawan (we need to figure out how and where we can provide these citations)

3. Guideline 2.1 - Information Needed

Issue Description: We need more information to continue the review.

Next Steps: Provide detailed answers to the following questions:

- Does your app send user's personal data to third party AI?
- If so, please specify the personal data that will be shared. 

Owner: Prafulla (I will include the details in next submission that “App does not invoke any third party AI so we do not send any user’s personal data to any third Party. The whole exercise recommendation engine in built in-house and moovvfit owns the engine, no third party involved”)



~ Best Regards,
Prafulla Joshi
Disclaimer: The information transmitted is intended for the person or entity to which it is addressed and may contain confidential, privileged or copyrighted material or attorney work product. If you receive this in error, please contact the sender and delete the material from any computer. Any comments or statements made are not necessarily those of Patheya Technologies Pvt. Ltd. All e-mails may be monitored or recorded.
Pawan Deshmukh <pawan.deshmukh@gmail.com>	Sat, Aug 29, 2026 at 10:04 PM
To: "Prafulla Joshi (Patheya)" <prafulla@patheya.tech>
Cc: moovv fit <fitmoovv@gmail.com>, "Shantanu Choudhary (Patheya)" <shantanu@patheya.tech>, "Devang Shirode (Patheya)" <devang@patheya.tech>, "Sudhanshu Kulkarni (Patheya)" <Sudhanshu@patheya.tech>, rahul jain <u2mailrahul@gmail.com>, "ujwal.parker@gmail.com" <ujwal.parker@gmail.com>, "Kundan Chaudhari (Patheya)" <kundan@patheya.tech>
Hi Prafulla, 

Thanks - We are a general wellness and fitness app. We are not a medical app right now and don't intend to go that direction. So all our changes ( if required should be in that direction)

As a first step we want to understand what exactly Apple saw on the app that led to that conclusion. Apple routinely declines to tell developers which specific content triggered a 1.4.1 rejection
Reply in Resolution Center with a specific, answerable question, not an open one. Reviewers will confirm or deny a proposition far more readily than write an analysis. Something like: We believe the flagged content is the 'How it helps' description on the exercise detail screen (screenshot attached). Can you confirm whether any other screen contributed?"
Important note: We do not want to mention in the app review that we are just a general wellness and fitness app.

Once we know that screen is contributing to it then we can resubmit the app after correcting the strings. 

"We have revised the exercise descriptions throughout the app to remove references to medical conditions, symptoms and therapeutic outcomes. Exercise guidance is now described in terms of movement, flexibility and comfort only. Clinical consultations continue to be delivered by licensed physiotherapists registered with their state council."

Let me know what your thoughts are and if there is any expert opinion here.




[Quoted text hidden]
--
Thanks,
PD
"In the battle between the river and the rock, the river always wins not through force but through perseverance."
Prafulla Joshi (Patheya) <prafulla@patheya.tech>	Mon, Aug 31, 2026 at 8:54 AM
To: Pawan Deshmukh <pawan.deshmukh@gmail.com>
Cc: moovv fit <fitmoovv@gmail.com>, "Shantanu Choudhary (Patheya)" <shantanu@patheya.tech>, "Devang Shirode (Patheya)" <devang@patheya.tech>, "Sudhanshu Kulkarni (Patheya)" <Sudhanshu@patheya.tech>, rahul jain <u2mailrahul@gmail.com>, "ujwal.parker@gmail.com" <ujwal.parker@gmail.com>, "Kundan Chaudhari (Patheya)" <kundan@patheya.tech>
Good morning, Yes aligned with all the mentioned understandings. 
We will first rectify the IAP error which Apple review team is saying that, it’s not related to whether the IAP Product is approved or not. So we will look into that today on priority.

Additionally, the links from the Apple Review team asks us to check “Product Configuration” and “Missing information” if any. 
When I checked Business > Agreement Tab there is an alert saying updated aggrement has to be accepted by “Account Holder”. Below the screen shot.

Could you please accept that agreement there? The link to “account” in this alter shows second screen, for your reference. 

PastedGraphic-1.png 

PastedGraphic-2.png
[Quoted text hidden]
Devang Shirode (Patheya) <devang@patheya.tech>	Mon, Aug 31, 2026 at 12:31 PM
To: Pawan Deshmukh <pawan.deshmukh@gmail.com>
Cc: moovv fit <fitmoovv@gmail.com>, "Shantanu Choudhary (Patheya)" <shantanu@patheya.tech>, "Sudhanshu Kulkarni (Patheya)" <Sudhanshu@patheya.tech>, rahul jain <u2mailrahul@gmail.com>, "ujwal.parker@gmail.com" <ujwal.parker@gmail.com>, "Kundan Chaudhari (Patheya)" <kundan@patheya.tech>, "Prafulla Joshi (Patheya)" <prafulla@patheya.tech>
Hi Pawan,
Apple rejected the app because some of the health and exercise advice does not include a source or a reminder to consult a doctor.
We found that this applies to the exercise information in the app and the AI assistant. Both provide health-related advice, but currently do not show where the information comes from or include a medical disclaimer.
Recommended fix: Add a source link to each piece of health or exercise advice.
For example:
Before:
“Strengthens the muscles around the knee and hip, helping with everyday activities such as standing up and climbing stairs.”
After:
Same advice, with a source such as:
Source: Versus Arthritis — Knee Exercises
[Source link]
This will show a clickable “Source ↗” link along with a disclaimer next to the advice. This directly addresses what Apple has asked us to add.
What we need from you:
Please confirm the trusted medical/clinical source that your physio team used for this exercise information.
In start we will start will few exercises and based on that we will scale up things. 
Thanks,
Devang Shirode 
From: Prafulla Joshi (Patheya) <prafulla@patheya.tech>
Sent: Monday, August 31, 2026 8:54 AM
To: Pawan Deshmukh <pawan.deshmukh@gmail.com>
Cc: moovv fit <fitmoovv@gmail.com>; Shantanu Choudhary (Patheya) <shantanu@patheya.tech>; Devang Shirode (Patheya) <devang@patheya.tech>; Sudhanshu Kulkarni (Patheya) <Sudhanshu@patheya.tech>; rahul jain <u2mailrahul@gmail.com>; ujwal.parker@gmail.com <ujwal.parker@gmail.com>; Kundan Chaudhari (Patheya) <kundan@patheya.tech>
Subject: Re: iOS App - v1.0.4 - Review comments from Apple and our action items
 
[Quoted text hidden]
Prafulla Joshi (Patheya) <prafulla@patheya.tech>	Wed, Sep 2, 2026 at 4:12 PM
To: "Devang Shirode (Patheya)" <devang@patheya.tech>, Pawan Deshmukh <pawan.deshmukh@gmail.com>, moovv fit <fitmoovv@gmail.com>, rahul jain <u2mailrahul@gmail.com>, "ujwal.parker@gmail.com" <ujwal.parker@gmail.com>, "Kundan Chaudhari (Patheya)" <kundan@patheya.tech>, "Sudhanshu Kulkarni (Patheya)" <Sudhanshu@patheya.tech>, "Shantanu Choudhary (Patheya)" <shantanu@patheya.tech>
Hi @Everyone
We are one step ahead in terms of end-to-end working of our IAP Product purchase.
Along with reference citations added to the app as well.
The latest app (v1.0.7) has been pushed to Test Flight and then released for Apple Review.

Ref screen recording for IAP - https://drive.google.com/file/d/1UHk968LDdMBuGtFYsQdSP452LGFnh8xb/view?usp=share_link 

Regards,
Prafulla


[Quoted text hidden]
[Quoted text hidden]
[Quoted text hidden]
<PastedGraphic-1.png> 
[Quoted text hidden]
[Quoted text hidden]