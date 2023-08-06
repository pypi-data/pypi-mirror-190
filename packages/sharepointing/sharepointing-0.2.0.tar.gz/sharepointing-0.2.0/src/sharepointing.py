import os
import ntpath
from urllib.parse import unquote
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

class sp_site:

    def __init__(self,site_url,username=os.environ.get('USERNAME'),password=os.environ.get('PASSWORD')):
        """
        Init constructor to build the class, requires only the @site_url
        it will take username and password as optional values, if two are not provided
        they will be retrieved from the local environment under $USERNAME and $PASSWORD name
        """

        self.site_url = site_url    # parameter for the sharepoint site
        self.username = username    # AD username
        self.password = password    # AD password
        self.ctx = self.ctx()       # Establish connection

        
    def ctx(self):
        try:
            ctx = ClientContext(self.site_url).with_credentials(UserCredential(f"{self.username}", f"{self.password}"))
            return ctx
        except:
            print("[Error] Could not connect to the SharePoint site, check your credentials and site url.")

        
    def read_file(self,file):
        """
        This function will read the content of the file before uploading it
        and returns a file_content object
        """
        try:
            with open(file, 'rb') as opened_file:
                file_content = opened_file.read()
                return file_content
        except:
            raise Exception("[Error] Could not read the file contents, make sure it's available with correct path.")

    def upload_file(self,local_file,remote_target_folder) -> bool:
        """
        Function to upload a @local_file within the local storage to a sharepoint @remote_target_url
        It shouldn't have the library url, so no http link and it has only / (backslashes) 
        This will return True if the file was uploaded successfully
        A good example is: "/teams/MarketingTeam/Shared Documents/General/Marketing Reports/"
        """

        # Read the file content
        file_content = self.read_file(local_file)

        # Extract the file's name
        file_name = ntpath.basename(local_file)

        try:
            # Get actual folder from server
            folder = self.ctx.web.get_folder_by_server_relative_url(remote_target_folder)
        except:
            raise Exception("[Error] Could not get to the folder, make sure the path is correct")
        
        try:
            # Upload file to that folder
            folder.upload_file(file_name, file_content).execute_query()

            return True
        except:
            raise Exception("[Error] Could not upload the file, make sure it's not read-only and you have the proper access.")

    def download_file(self,remote_file,local_target_folder) -> bool:
        """
        Function to download a @remote_file from a SharePoint site to the local folder @local_target_folder
        #Example#
        remote_file = "/teams/MarketingTeam/Shared Documents/General/Marketing Reports/data.csv"
        local_target_folder = "/home/username" # you can pass empty string to get the file where the code is running

        This will return True if the file was uploaded successfully
        """

        try:
            file_name = os.path.basename(remote_file)
            local_target_file = os.path.join(local_target_folder,file_name)
        except:
            raise Exception("[Error] Could not parse remote_file or local_target_folder, make sure the format is correct.")
        
        try:
            with open(local_target_file,'wb') as file:
                file = self.ctx.web.get_file_by_server_relative_url(remote_file).download(file).execute_query()

            return True
        except:
            raise Exception("[Error] Could not download the file, make sure the file exists and you have access to download it.")

def decode_link(full_link,option) -> str:
    """
    This function will take any full link from SharePoint and can give back two two options
    1 > The site_url
    2 > The target folder
    3 > Both as list
    Instructions: Using your browser, open your SharePoint site and navigate to the target folder
    Copy the link from the browser, and provide it here.
    """
    # Decode url
    url = unquote(full_link)

    # Find the end of the site's url 
    l1 = url.find('/Forms/AllItems.aspx?')
    path = url[:l1].split('/')

    # Extract the site's url
    site_url = '/'.join(path[0:len(path)-1])

    # Find the actual folder path within the site/library
    l1 = url.find('?id=')+4
    l2 = url.find('&viewid')

    # Extract the target folder
    target_folder = url[l1:l2]

    if option==1:
        return site_url
    elif option==2:
        return target_folder
    else:
        return site_url,target_folder
