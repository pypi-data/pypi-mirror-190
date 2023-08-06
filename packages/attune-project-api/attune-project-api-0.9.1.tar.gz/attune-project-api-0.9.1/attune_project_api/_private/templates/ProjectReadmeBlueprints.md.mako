<%page args="blueprints"/>
<%text>
## Project Blueprints
</%text>
% for blueprint in blueprints:

<%text>###</%text> ${blueprint.name}

% if blueprint.comment:
${blueprint.makeCommentMarkdown(topHeaderNum=4)}
% endif
% endfor