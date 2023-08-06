<%page args="makoGlobal, projectMetadata, params, niceParameterNames, files,
blueprints"/>
# ${projectMetadata.name}

${projectMetadata.makeCommentMarkdown(topHeaderNum=2)}

<%include file="ProjectReadmeBlueprints.md.mako" args="blueprints=blueprints"/>

<%include file="ProjectReadmeParameters.md.mako" args="params=params, niceParameterNames=niceParameterNames"/>

<%include file="ProjectReadmeFiles.md.mako" args="files=files"/>

<%include file="ProjectReadmeServerTribe.md.mako"
args=""/>

Thank you.
