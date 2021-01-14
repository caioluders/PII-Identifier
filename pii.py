import re
from burp import IBurpExtender
from burp import IScannerCheck
from burp import IScanIssue
from burp import ITab
from array import array
from java.io import PrintWriter
from javax.swing import JPanel, JTextField, JButton, JLabel, BoxLayout, JPasswordField, JCheckBox, JRadioButton, ButtonGroup, JSlider
from java.awt import GridLayout, BorderLayout


EXT_NAME = "PII Notifier"

class BurpExtender(IBurpExtender, IScannerCheck, ITab):
	def __init__(self):
		self.cpfcheck = True
		self.fullnamecheck = True
		self.rgcheck = True
		self.birthdaycheck = True
		self.requestcheck = True
		self.responsecheck = True

	def registerExtenderCallbacks( self, callbacks):# your extension code here
		callbacks.setExtensionName(EXT_NAME)
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()


		self._stdout = PrintWriter(callbacks.getStdout(), True)

		callbacks.registerScannerCheck(self)
		callbacks.addSuiteTab(self)

	
	def _get_matches(self, response) :
		matches = []
		start = 0
		reslen = len(response)
		#matchlen = len(match) 

		self._stdout.println(self._helpers.bytesToString(response)[0:20])
		return False

	def doPassiveScan(self, baseRequestResponse) :
		matches = self._get_matches( baseRequestResponse.getResponse() )
		
		return None


	def getUiComponent(self) :

		cpfcheck = self._callbacks.loadExtensionSetting("cpfcheck")
		rgcheck = self._callbacks.loadExtensionSetting("rgcheck")
		fullnamecheck = self._callbacks.loadExtensionSetting("fullnamecheck")
		birthdaycheck = self._callbacks.loadExtensionSetting("birthdaycheck")
		requestcheck = self._callbacks.loadExtensionSetting("requestcheck")
		responsecheck = self._callbacks.loadExtensionSetting("responsecheck")

		if cpfcheck :
			self.cpfcheck = (True if cpfcheck == "True" else False ) 
		if responsecheck :
			self.responsecheck = (True if responsecheck == "True" else False ) 
		if requestcheck :
			self.requestcheck = (True if requestcheck == "True" else False ) 
		if rgcheck :
			self.rgcheck = (True if rgcheck == "True" else False ) 
		if fullnamecheck :
			self.fullnamecheck = (True if fullnamecheck == "True" else False ) 
		if birthdaycheck :
			self.birthdaycheck = (True if birthdaycheck == "True" else False ) 

		self.panel = JPanel()
		self.main = JPanel() 

		self.main.setLayout(GridLayout(0,2))

		self.pii_types = JPanel()
		self.main.add(self.pii_types)
		self.pii_types.add(JLabel('PII Types'))
		self.cpf_checkbox = JCheckBox("CPF",self.cpfcheck)
		self.fullname_checkbox = JCheckBox("Full Name", self.fullnamecheck)
		self.rg_checkbox = JCheckBox("RG", self.rgcheck)
		self.birthday_checkbox = JCheckBox("Birthday", self.birthdaycheck)
		self.pii_types.add(self.fullname_checkbox)
		self.pii_types.add(self.birthday_checkbox)
		self.pii_types.add(self.rg_checkbox)
		self.pii_types.add(self.cpf_checkbox)

		self.check_panel = JPanel()
		self.main.add(self.check_panel)
		self.check_panel.add(JLabel("Checks"))
		self.request_checkbox = JCheckBox("Request",self.requestcheck)
		self.response_checkbox = JCheckBox("Response",self.responsecheck)
		self.check_panel.add(self.request_checkbox)
		self.check_panel.add(self.response_checkbox)

		self.slider_panel = JPanel()
		self.main.add(self.slider_panel)
		self.slider_panel.add(JLabel("Threshold"))
		self.threshold_slider = JSlider(JSlider.HORIZONTAL,0,100,50)
		self.slider_panel.add(self.threshold_slider)

		self.buttons = JPanel()
		self.main.add(self.buttons,BorderLayout.CENTER)

		self.save_button = JButton("Save", actionPerformed = self.savePressed)
		self.buttons.add(self.save_button)

		self.panel.add(self.main)

		return self.panel

	def savePressed(self, event) :
		self._callbacks.saveExtensionSetting("cpfcheck",str(self.cpf_checkbox.isSelected()))
		self._callbacks.saveExtensionSetting("rgcheck",str(self.rg_checkbox.isSelected()))
		self._callbacks.saveExtensionSetting("fullnamecheck",str(self.fullname_checkbox.isSelected()))
		self._callbacks.saveExtensionSetting("birthdaycheck",str(self.birthday_checkbox.isSelected()))
		self._callbacks.saveExtensionSetting("requestcheck",str(self.request_checkbox.isSelected()))
		self._callbacks.saveExtensionSetting("responsecheck",str(self.response_checkbox.isSelected()))
		return



	def getTabCaption(self) :
		return EXT_NAME 

	def consolidateDuplicateIssues(self, existingIssue, newIssue):
		if existingIssue.getIssueName() == newIssue.getIssueName():
			return -1

		return 0

	def extensionUnloaded(self):
		self._stdout.println("Extension was unloaded")

class CustomScanIssue (IScanIssue):
	def __init__(self, httpService, url, httpMessages, name, detail, severity):
		self._httpService = httpService
		self._url = url
		self._httpMessages = httpMessages
		self._name = name
		self._detail = detail
		self._severity = severity

	def getUrl(self):
		return self._url

	def getIssueName(self):
		return self._name

	def getIssueType(self):
		return 0

	def getSeverity(self):
		return self._severity

	def getConfidence(self):
		return "Certain"

	def getIssueBackground(self):
		pass

	def getRemediationBackground(self):
		pass

	def getIssueDetail(self):
		return self._detail

	def getRemediationDetail(self):
		pass

	def getHttpMessages(self):
		return self._httpMessages

	def getHttpService(self):
		return self._httpService

