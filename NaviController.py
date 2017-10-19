"""
author: Abdurrahim Burak Tekin
version: 19.10.2017
"""

from xml.etree import ElementTree
import NaviModel
import NaviView
import requests
from PySide.QtGui import QWidget


class Controller(QWidget):
    """
    the controller of MVC
    """

    def __init__(self, parent=None):
        """
        __init__ method
        :param parent: parent object of controller-widget
        """
        super().__init__(parent)
        self.view = NaviView.Ui_Form()
        self.view.setupUi(self)

        self.model = NaviModel.Model()
        self.view.submitButton.clicked.connect(self.submit)

        self.req = ""

    def clear_view(self):
        """
        clears every label & input
        """
        self.view.outputNavi.clear()

    def submit(self):
        """
        starts navigation by buttonclick
        """

        # call clear_view()
        self.clear_view()

        # try-catch for status -> STATUS: INDEX_ERROR if error occured
        try:
            # both inputs are taken and put into API
            origin = self.view.vonInput.text()
            destination = self.view.bisInput.text()

            # if-wheel for choosing between JSON / XML
            if self.view.dialChoose.value() < 50:
                # using API with JSON
                url = "https://maps.googleapis.com/maps/api/directions/json" \
                      + "?origin=" + origin \
                      + "&destination=" + destination \
                      + "&language=" +self.model.LANG \
                      + "&key=" + self.model.KEY
            else:
                # using API with XML
                url = "https://maps.googleapis.com/maps/api/directions/xml" \
                      + "?origin=" + origin \
                      + "&destination=" + destination \
                      + "&language=" + self.model.LANG \
                      + "&key=" + self.model.KEY

            # headers = {"content-type": "application/json"}
            params = {"origin": origin,
                      "destination": destination,
                      "sensor": "false"}
            # results are taken
            self.req = requests.get(url, params, verify=False)

            # if JSON is the chosen format -> JSON-filter
            if self.view.dialChoose.value() < 50:
                # results as JSON-format
                outputjson = self.req.json()

                # general information is taken
                startjson = "Start: " + outputjson["routes"][0]["legs"][0]["start_address"]
                endjson = "Ziel: " + outputjson["routes"][0]["legs"][0]["end_address"]
                distancejson = "Entfern.: " + outputjson["routes"][0]["legs"][0]["distance"]["text"]
                durationjson = "Dauer: " + outputjson["routes"][0]["legs"][0]["duration"]["text"]

                # appending information to label (better than setText() -> does replace text)
                self.view.outputNavi.append(startjson + "<br>" +
                                            endjson + "<br>" +
                                            distancejson + "<br>" +
                                            durationjson + "<br>")

                # shows which mode is active
                self.view.outputNavi.append(" MODE: <b>JSON<b>" + "<br>")

                # route instructions are taken
                for index in outputjson["routes"][0]["legs"][0]["steps"]:
                    instrjson = index["html_instructions"]
                    distjson = index["distance"]["text"]
                    durjson = index["duration"]["text"]
                    # appending instructions to label (better than setText() -> does replace text)
                    self.view.outputNavi.append(instrjson + " | " + distjson + " - " + durjson)

            # if XML is the chosen format -> XML-filter
            else:
                # results as XML-format
                outputxml = ElementTree.fromstring(self.req.content)

                # general information is taken
                startxml = outputxml.find("route").find("leg").find("start_address").text
                endxml = outputxml.find("route").find("leg").find("end_address").text
                distancexml = outputxml.find("route").find("leg").find("distance").find("text").text
                durationxml = outputxml.find("route").find("leg").find("duration").find("text").text

                # appending information to label (better than setText() -> does replace text)
                self.view.outputNavi.append("Start: " + startxml + "<br>" +
                                            "Ziel: " + endxml + "<br>" +
                                            "Entfern.: " + distancexml + "<br>" +
                                            "Dauer: " + durationxml + "<br>")

                # shows which mode is active
                self.view.outputNavi.append("MODE: <b>XML<b>" + "<br>")

                # route instructions are taken
                for all in outputxml.find("route").find("leg").findall("step"):
                    instrxml = all[5].text
                    distxml = all[6][1].text
                    durxml = all[4][1].text

                    # appending instructions to label (better than setText() -> does replace text)
                    self.view.outputNavi.append(instrxml + " | " + distxml + " - " + durxml)

        except IndexError:
            # setText() to "STATUS: ERROR" if error occured
            self.view.statusLabel.setText("Status: FAILED")
            self.view.outputNavi.setText("<b>IndexError:<b> Please try again.")
            # raise IndexError
        except TypeError:
            # setText() to "STATUS: ERROR" if error occured
            self.view.statusLabel.setText("Status: FAILED")
            self.view.outputNavi.setText("<b>TypeError:<b> Please try again.")
            # raise TypeError
        except AttributeError:
            # setText() to "STATUS: ERROR" if error occured
            self.view.statusLabel.setText("Status: FAILED")
            self.view.outputNavi.setText("<b>AttributeError:<b> Please try again.")
            # raise AttributeError
        else:
            # setText() to "STATUS: OK" if navigation worked OK
            self.view.statusLabel.setText("Status: OK")

    # used pylint NaviController.py in terminal for code-rating: 8.83/10
    # Markus gave me nice tips about writing a beautiful code - Thank you Markus Lint 10/10 :D
