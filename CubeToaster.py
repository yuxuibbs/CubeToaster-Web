from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



#################################################################################
# Configurations
app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.config['SECRET_KEY'] = 'cubetoaster'

startHTML = '''
  <html>
    <head>
      <style>
        table {
          border-collapse: collapse;
          height: 100%;
          width: 100%;
        }

        table, th, td {
          border: 3px solid black;
        }

        @media print {
          table {
            page-break-after: always;
          }
        }

        .cutoffs td {
          border: 0;
          font-weight: bold;
        }

        .compName {
          font-size: 32pt;
          font-weight: bold;
          height: 65px;
        }

        .labels {
          font-size: 24pt;
          font-weight: bold;
        }

        .attempt {
          font-size: 36pt;
          font-weight: bold;
          text-align: center;
        }

        .event, .personID {
          font-size: 36pt;
          font-weight: bold;
          width: 60px;
        }

        .round, .heat {
          font-size: 24pt;
          font-weight: bold;
          text-align: left;
        }

        .personName {
          font-size: 40pt;
          font-weight: bold;
          height: 64px;
        }

        .attemptNumber {
          width: 60px;
        }

        .initial, .scrambler {
          width: 100px;
        }
      </style>
    </head>
    <body>
'''

ao5Table = '''
      <table>
        <tr>
          <th colspan="6" class="compName">competitionName</th>
        </tr>
        <tr>
          <th colspan="1" class="personID"></th>
          <th colspan="3" class="event">eventName</th>
          <th colspan="1" class="heat">G: groupNumber</th>
          <th colspan="1" class="round">R: roundNumber</th>
        </tr>
        <tr>
          <th colspan="6" class="personName">competitorName</th>
        </tr>
        <tr class="labels">
          <th colspan="1" class="scrambler">Scr</th>
          <th colspan="1" class="attemptNumber">#</th>
          <th colspan="2">Results</th>
          <th colspan="1" class="initial">Judge</th>
          <th colspan="1" class="initial">Comp</th>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">1</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">2</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="cutoffs">
          <td colspan="1"></td>
          <td colspan="1"></td>
          <td colspan="1">Cutoff: cutoffTime</td>
          <td colspan="1">Time Limit: timeLimit</td>
          <td colspan="1"></td>
          <td colspan="1"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">3</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">4</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">5</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
        <tr class="empty">
          <td colspan="6"></td>
        </tr>
        <tr class="attempt">
          <td colspan="1"> </td>
          <td colspan="1">E</td>
          <td colspan="2"> </td>
          <td colspan="1"> </td>
          <td colspan="1"> </td>
        </tr>
      </table>
'''

endHTML = '''
    </body>
  </html>
'''


#################################################################################
# Forms
class RegistrationForm(FlaskForm):
    compName = StringField('Competition name to display:')
    roundNum = StringField('Round number:')
    groupNum = StringField('Group number:')
    event = StringField('Event Name:')
    cutoff = StringField('Cutoff:')
    timeLimit = StringField('Time limit:')
    names = StringField('Insert list of people separated by a comma (do not use comma space, only comma):', validators = [DataRequired()])
    submit = SubmitField('Submit')

#################################################################################
# Helper functions
# def createDataStructure(data):
#     compName = data['shortName']
#     people = data['persons']
#     compEvents = data['events']
def addScoreSheet(updatedScoreSheetTable, compName, eventName, roundNum, groupNum, name, cutoff, timeLimit):
    updatedScoreSheetTable = updatedScoreSheetTable.replace("competitionName", compName
                                                  ).replace("eventName", eventName
                                                  ).replace("roundNumber", roundNum
                                                  ).replace("groupNumber", groupNum
                                                  ).replace("cutoffTime", cutoff
                                                  ).replace("timeLimit", timeLimit
                                                  ).replace("competitorName", name)
    return updatedScoreSheetTable

def makeScoreSheets(compName, roundNum, groupNum, event, names, cutoff, timeLimit):
    '''
    Creates string with HTML that contains all of the necessary
    score sheets for the first round of the competition
    '''
    scoreSheetList = []
    updatedScoreSheetTable = ao5Table
    for _, person in enumerate(names.split(',')):
        scoreSheetList.append(addScoreSheet(updatedScoreSheetTable, compName, event, roundNum, groupNum, person, cutoff, timeLimit))


    scoreSheets = str.join("\n", scoreSheetList)

    return startHTML + scoreSheets + endHTML


###############################################################################
## Routes and view functions

@app.route('/', methods = ['GET', 'POST'])
def home():
    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        data = makeScoreSheets(request.form.get('compName'),
                               request.form.get('roundNum'), request.form.get('groupNum'),
                               request.form.get('event'), request.form.get('names'),
                               request.form.get('cutoff'), request.form.get('timeLimit'))
        return render_template('view_heats.html', data=data)
    return render_template('scorecards.html', form=form)


if __name__ == '__main__':
    # app.run(host = '0.0.0.0', port = int(os.getenv('PORT', 5001)))
    app.run()
