# Sharepointing
A library to establish connection to sharepoint. Then operate on this connection. Right now it's only possible to upload files.

This library depends on office 365 library, and it will use active directory authentication to connect to SharePoint.

## Installation
In order to install this library you need to obtain an `SSH code`

Use pip to install this library from Github:

    pip install sharepointing

## Requirements
First you need to initialize the the sharepoint connection, which is an object.
You have two options, either use embedded credentials in environment variables:

`USERNAME` for office365 email

`PASSWORD` for office365 password


Then you can use this call:

    sp = sharepointing.sp_site(site_url)

The second option is to provide the credentials in the class call:

    sp = sharepointing.sp_site(site_url,username,password)

Once the object is created successfully, you can call use `upload_file` method to upload the files to sharepoiont

## decode_link function
This function will take any full link from SharePoint and can give back two two options
1 > The site_url
2 > The target folder
3 > Both as list
Instructions: Using your browser, open your SharePoint site and navigate to the target folder
Copy the link from the browser, and provide it here.

## Example 1 - upload_file
    site_url = "https://companysite.sharepoint.com/teams/teamsname"
    target = "/teams/teamsname/Shared Documents/General/"
    file = 'file.txt'
    sp = sharepointing.sp_site(site_url)
    sp.upload_file(file,target)

## Example 2 - decode_link
    full_link = "https://companysite.sharepoint.com/teams/teamsname/Shared%20Documents/Forms/AllItems.aspx?id=%2Fteams%teamsname%2FShared%20Documents%2FGeneral%2FSales%20Management%2F99%2E%20Resources%2F02%2E%20First%20Region&viewid=ecdf0311%2De700%2D4d9b%2Db7d3%2D6eaecaf18c76"
    site_url = decode_link(full_link,1)
    target = decode_link(full_link,2)

## Example 3 - download_file
    # Get the target url of where file is
    sp_url = "https://excellentproject.sharepoint.com/teams/MarketingTeam/Shared%20Documents/Forms/AllItems.aspx?id=%2Fteams%2FMarketingTeam%2FShared%20Documents%2FGeneral%2FMarketing%20Reports%2Fdata&viewid=ecdf0311dddd9dbddd7d3%2Dddddddsad"

    # Extract the site url and the target folder
    site_url,target_folder = decode_link(sp_url,3)

    # Define the file name 'myfile.csv' and construct its full path
    remote_file = os.path.join(target_folder,'myfile.csv')

    # Local folder path, can be referring to anything
    local_folder = ""

    # Initialize the SharePoint site object
    sp = sp_site(site_url)

    # Execute the recieve
    sp.download_file(remote_file,local_folder)

