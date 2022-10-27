#############################################################
#                                                           #
#                   Copyright Bluebotlabz                   #
#                                                           #
#############################################################
import os
import math
import requests
import xml.etree.ElementTree as xml
utilityVersion = "v1.0.0"
verboseDebug = False

def addSlash (path):
    if (path[-1] != "/"):
        path += "/"
    return path



print("==================================================")
print("=            Phonak Target Downloader            =")
print("="*(47-len(utilityVersion)) + " " + utilityVersion + " =")

disclaimer = [
    "DISCLAIMER",
    "",
    "I (Bluebotlabz), do not take any responsability for what you do using this software",
    "Phonak is a trademark of Sonova AG",
    "Sonova is a trademark of Sonova AG",
    "Phonak is a subsidiary of Sonova AG",
    "Phonak Target is created by Phonak",
    "All rights and credit go to their rightful owners. No copyright infringement intended."
    "",
    "Bluebotlabz and this downloader are not affiliated with or endorsed by Phonak or Sonova AG",
    "This is an UNOFFICIAL downloader and use of the software downloaded using it may be limited"
]

disclaimerWidth = 150
print("\n\n")
print ("="*disclaimerWidth)
for line in disclaimer:

    paddedLine = line
    leftPad = (disclaimerWidth-len(paddedLine))/2
    rightPad = (disclaimerWidth-len(paddedLine))/2

    if (leftPad % 1 != 0):
        leftPad = math.floor(leftPad) + 1
        rightPad = math.floor(rightPad)
    
    leftPad = int(leftPad)
    rightPad = int(rightPad)

    print("=" + " "*(leftPad-1) + line + " "*(rightPad-1) + "=")
print ("="*disclaimerWidth)
input("Press enter to continue...")
print("\n\n")



print("Fetching Data...")
xmlns = "{http://cocoon.phonak.com}"
xmlData = requests.get("https://p-svc1.phonakpro.com/1/ObjectLocationService.svc/FittingApplicationInstaller/index?appName=Phonak%20Target&appVer=6.0.1.695&dist=Phonak&country=GB&subKeys=").text
data = xml.fromstring(xmlData)

# Get latest version number (Gets full version from xml and removes the fourth version number as that is not used in files)
latestVersion = '.'.join((data[0].find(xmlns + "UpdateVersion").find(xmlns + "Version").text).split(".")[:-1])

print("\n\n")
validVersions = [
    (latestVersion, 'The latest available Phonak Target verion'),
    ('6.2.8', 'The last version of Phonak Target compatible with the iCube (obsolete proprietary hearing aid programmer)'),
    ('manual', 'Manually specify a version (WARNING: ADVANCED USERS ONLY)')
]

outputDir = ''
while not outputDir:
    outputDir = input("Enter an output directory: ")
    if (input("Confirm download path (" + outputDir + ") [Y/n] ") == "n"):
        outputDir = ''

targetVersion = ''
while not targetVersion:
    print("\n\n")
    versionIndex = 0
    for version in validVersions:
        print(str(versionIndex) + ". " + version[0] + "\t" + version[1])
        versionIndex += 1
    
    try:
        targetVersion = int(input("Please select a version: "))
    except ValueError:
        targetVersion = -1
    
    if (targetVersion >= 0 and targetVersion < len(validVersions)):
        if (input("You have selected version (" + validVersions[targetVersion][0] + ") are you sure you want to download it? [Y/n] ") == "n"):
            targetVersion = ''
        else:
            targetVersion = validVersions[targetVersion][0]
    else:
        print("The version you have selected is invalid.\nPlease try again.")
        targetVersion = ''


print("\n\n")

if (targetVersion == 'latest'):
    targetVersion = latestVersion
elif (targetVersion == 'manual'):
    targetVersion = ''
    while not targetVersion:
        targetVersion = input("Please enter manual target version: ")
        if (len(targetVersion.split('.')) > 3 or not targetVersion.replace('.', '').isdecimal()):
            print("The version you have selected is invalid.\nPlease try again. (hint: it should be in a similar format to a.b.c where a, b, and c are integers)")
        elif (input("You have selected version (" + targetVersion + ") are you sure you want to download it? [Y/n] ") == "n"):
            targetVersion = ''

# Get CDN/Download location
phonakCDNPath = data[0].find(xmlns + "Location").text

# Download "filelist" and update metadata
print ("Downloading directory index")
filesToDownload = {}
for child in data[0].find(xmlns + "ContentInfos"):
    # Construct paths
    filesToDownload[(addSlash(outputDir) + child.find(xmlns + "Key").text).replace(latestVersion, targetVersion)] = (addSlash(phonakCDNPath) + addSlash(child.find(xmlns + "RemotePath").text) + child.find(xmlns + "Key").text).replace(latestVersion, targetVersion)

# Download and save the files
print("Downloading " + str(len(filesToDownload.keys())) + " files")
currentFile = 1
for fileToDownload in filesToDownload.keys():
    os.makedirs('/'.join(fileToDownload.split("/")[:-1]), exist_ok=True) # Create path if it doesn't exist

    print("Downloading " + fileToDownload.split("/")[-1] + " (" + str(currentFile) + "/" + str(len(filesToDownload.keys())) + ")")
    if (verboseDebug):
        print(filesToDownload[fileToDownload])
    fileData = requests.get(filesToDownload[fileToDownload]) # Get file
    if (fileData.status_code != 404):
        with open(fileToDownload, 'wb') as file: # Write file content
            file.write(fileData.content)
    else:
        print("\n\nERROR: 404 File not found")
        exit()

    currentFile += 1

print("\n\nDownload Complete!")
