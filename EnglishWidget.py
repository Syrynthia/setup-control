from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class EnglishWidget(QWidget):
    def __init__(self, parent, img1, img2, img3):
        super(EnglishWidget, self).__init__(parent)
        tab_layout = QVBoxLayout()

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)

        text_edit.textCursor().insertHtml('<center><h1> Setup control data analysis application manual </h1></center><br> ')
        text_edit.textCursor().insertHtml('<h2>Importing data</h2> <br>')
        text_edit.textCursor().insertHtml('<p>To import data select File menu and choose Import→Multiple '
                                          'Patients→Select Multiple Files or Import→Multiple Patients→Select Folder. '
                                          'The first option allows to choose multiple files from a certain folder – '
                                          'either through selecting the files with the mouse (holding down Shift allows '
                                          'to choose all the files in range from the first to the second selected whilst '
                                          'holding down Ctrl allows for the selection of multiple files at any locations '
                                          'throughout the folder) or through pressing Ctrl+A to select all the files '
                                          'in the folder. The second option will let the user analyse all the files '
                                          'in the selected directory. The application is set to undo the correction '
                                          'of the shift values with the parameters given in the Preferences dialog. '
                                          'The correction will occur after a set number of sessions. That number can '
                                          'be changed in the Preferences dialog. </p><br>')
        text_edit.textCursor().insertHtml('<p>Afterwards the application will calculate the averages and standard '
                                          'deviations for each of the coordinates of the distance vector from the '
                                          'isocenter. The calculation results will be presented  in a table as well as '
                                          'on a plot. To view the plot for the particular shift direction simply select '
                                          'the checkbox adjacent to a label with the corresponding name on right side '
                                          'of the plot frame.</p><br>')
        text_edit.textCursor().insertImage(img1)
        text_edit.textCursor().insertHtml('<br><p>It is possible to view values after the correction undoing for a single '
                                          'file. To achieve that simply select  File→Import→Single Patient. A new '
                                          'window will open in which you will be able to see the calculated values '
                                          'in a table, underneath the table there will be the results of the average '
                                          'and standard deviation calculations and under that there will be a plot '
                                          'of the shift values for concurrent dates of the medical sessions. '
                                          'To view those values select the appropriate checkboxes on the right.</p><br>')
        text_edit.textCursor().insertImage(img2)
        text_edit.textCursor().insertHtml('<br><h2>Saving the data</h2> <br>')
        text_edit.textCursor().insertHtml('<p>The application allows for saving the data to a .csv (comma-separated '
                                          'values) file. This format allows for easy further analysis in a spreadsheet.'
                                          ' To present the data in the best way select space as the separating value '
                                          'and quotation mark (“) as the text delimiter. Saving the data this way '
                                          'requires selecting  File → Save... → data to a .csv file, navigating in the '
                                          'pop-up dialog to the appropriate directory and inputting the name of the '
                                          'file at the bottom of the dialog. The application will add the extension '
                                          'by default.</p><br>')
        text_edit.textCursor().insertHtml('<p>It is possible to save the plot to a file as well. Simply select  '
                                          'File → Save... → plot and proceed as above. The file formats that '
                                          'may be used to save the plot are: .png (portable network graphics), .pdf '
                                          '(portable document format), .svg (scalable vector graphics), .ps (PostScript) '
                                          'and .eps (encapsulated PostScript). To use any of those formats select it '
                                          'in the dropdown list at the bottom of the pop-up dialog. The appropriate '
                                          'extension will automatically be added to the input file name or it may be '
                                          'manually added by the user. The application will ignore any attempts to '
                                          'save the plot in a format different from the ones mentioned above.</p><br>')
        text_edit.textCursor().insertHtml('<h2>Preferences</h2> <br>')
        text_edit.textCursor().insertHtml('<p>The parameters of the data analysis may be adjusted. After selecting '
                                          'Edit → Preferences a non-modal dialog will show in which the user may '
                                          'change three parameters.</p><br>')
        text_edit.textCursor().insertImage(img3)
        text_edit.textCursor().insertHtml('<br><p>The first parameter is the threshold after which the corrections '
                                          'are applied. The default value of the threshold is 0.3 cm. To change '
                                          'the value input the new one into the text area (the text area will only '
                                          'accept floating point values).</p><br>')
        text_edit.textCursor().insertHtml('<p>The second parameter is the number of sessions in each file that '
                                          'have been skipped before the correction. The default value of this '
                                          'parameter is 3. To change the value input the new one into the text area '
                                          '(the text area will only accept integer values).</p><br>')
        text_edit.textCursor().insertHtml('<p>The last parameter is the maximum number of sessions that will be taken '
                                          'into calculating the mean avarages and the standard deviations. The default '
                                          'value is all the sessions in each file. To change the value input '
                                          'the new one into the text area (the text area will only accept '
                                          'integer values). To select all the sessions in each file put in 0 into '
                                          'the text area.</p><br>')
        text_edit.textCursor().insertHtml('<p>Selecting Apply will change the values, but it will not close the dialog. '
                                          'Selecting Ok will change the values and close the dialog. After the dialog '
                                          'closes the data will automatically refresh itself with the new '
                                          'parameters.</p><br>')
        text_edit.textCursor().insertHtml('<h2>Keyboard shortcuts</h2> <br>')
        text_edit.textCursor().insertHtml('<table>'
                                          '<tr>'
                                          '<th><br>			Shortcut		</th>'
                                          '<th><br>			Action		</th>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + O		</td>'
                                          '<td><br>			Import data from multiple files	</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + F<		</td>'
                                          '<td><br>		Import data from all the files in the selected directory</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + A		</td>'
                                          '<td><br>			Import data for a single patient		</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + S		</td>'
                                          '<td><br>			Save data to a .csv file	</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + L		</td>'
                                          '<td><br>			Save the plot	</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + H		</td>'
                                          '<td><br>			Help		</td>'
                                          '</tr>'
                                          '<tr>'
                                          '<td><br>			Ctrl + P		</td>'
                                          '<td><br>			Open the Preferences dialog		</td>'
                                          '</tr>'
                                          '</table>')

        text_edit.moveCursor(QTextCursor.Start)
        tab_layout.addWidget(text_edit)
        self.setLayout(tab_layout)