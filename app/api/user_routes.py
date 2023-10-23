from . import api
from ..models import User, Projects
from flask import request
from .apiauthhelper import token_auth


@api.post('/creatproject')
@token_auth.login_required
def createProject():
    data = request.json

    admin_id = data['admin_id']
    project_name = data['project_name']
    description = data['description']
    duration = data['duration']
    industries = data['industries']
    looking_for = data['looking_for']
    team = data['team_needed']

    project = Projects.query.filter_by(name = project_name).first()
    if project:
        return {
            'status': 'not ok',
            'message': 'That project already exists.'
        }, 400
    project = Projects(admin_id=admin_id, name=project_name, description=description, duration=duration, industries=industries, looking_for=looking_for)

    # Adresses what roles the project needs. Default values in db are True
    if team['productManager'] == False:
        project.need_pm = False
    if team['productDesigner'] == False:
        project.need_designer = False
    if team['developer1'] == False and team['developer2'] == False:
        project.need_dev = False

    project.saveToDB()
    #Check to see if the project saved to the database successfully
    projectsaved = Projects.query.filter_by(name=project_name).first()
    if projectsaved:
        user = User.query.get(admin_id)
        user.current_project_id = projectsaved.id
        user.saveToDB()
        return {
            'status': 'ok',
            'message': 'Project successfully created!',
            'project': projectsaved.to_dict()
        }, 200
    else:
        return {
            'status': 'not ok',
            'message': 'Potential error in project creation or querying.'
        }, 400


@api.post('/add-user-to-project')
@token_auth.login_required
def addUserToProject(user_id, project_id):

    # Query for the user and project
    user = User.query.get(user_id).first()
    project = Projects.query.get(project_id)

    # Check if user or project does not exist
    if user is None or project is None:
        return {
            'status': 'not ok',
            'message': 'User or project not found.'
        }, 400

    # Check if the user is already part of another project
    if user.current_project_id is not False:
        return {
            'status': 'not ok',
            'message': 'User is already part of a different project.'
        }, 400

    # Add user to the project
    user.current_project_id = project.id
    user.saveToDB()

    return {
        'status': 'ok',
        'message': 'User added to project successfully'
    }, 200

@api.post('/removeprojectuser')
@token_auth.login_required
def removeProjectUser():
    data = request.json

    project_id = data['project_id']
    user_id = data['user_id']

    project = Projects.query.get(project_id)
    user = User.query.get(user_id)

@api.get('/getteam/<int:proj_id>')
@token_auth.login_required
def getTeam(proj_id):
    project = Projects.query.get(proj_id)

    if project:
        members = project.members
        return {
            'status': 'ok',
            'members': [member.to_dict() for member in members],
            'team_size': len(members)
        }
    
@api.get('/getteamsbrowser')
@token_auth.login_required
def teamsBrowser():
    projects = Projects.query.all()
    users = User.query.all()

    return {
        'status': 'ok',
        'projects': [project.to_dict() for project in projects],
        'users': [user.to_dict() for user in users],
        'number_of_projects': len(projects),
        'number_of_users': len(users)
    }