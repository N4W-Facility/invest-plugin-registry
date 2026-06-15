.. _review_process:

=====================
Plugin Review Process
=====================

**Intended Audience:** This documentation is geared towards members of the Plugin Reviewer
Pool, as a reference / refresher for the plugin review process.

Review Rubric
-------------

**Reviewer Instructions:** Please review the plugin submission pull request based
on the following criteria:

- [ ] The only modification to ``plugins.json`` was to add a new entry for this plugin;
  no other changes were made
- [ ] The submitter included all required information in the PR description, including:

  - [ ] The plugin repo URL;
  - [ ] A brief description of the plugin's motivation and context;
  - [ ] Acknowledgment of the Code of Conduct

- [ ] The plugin is germane to NatCap's work, broadly (it has to do with nature and/or
  nature's benefits to people)
- [ ] The plugin has documentation and documents data needs
- [ ] The plugin's documentation appears relevant to the plugin's description
- [ ] The plugin's name is unique and appropriate (it adheres to the
  :doc:`Code of Conduct <code_of_conduct>`)

**If any of the above criteria were not met, please provide a brief explanation:**

[Explanation of missing / unmet criteria]

----

Submitting a Review
-------------------

After reading through the content of the PR submission body and checking relevant files in
the plugin repository, please also double-check the files changed by the PR. Only
``plugins.json`` should have been modified. To submit a review:

- On the PR, go to the "Files changed" tab
- Click the green "Submit review" button
- If the submission met all of the criteria in the above rubric:

  - In the "Leave a comment" section, write a brief comment that tags the submitter (e.g.
    ``@natcap-bot``) and thanks them for their submission
  - Select the "Approve" radio button
  - Click the green "Submit review" button
  - Back in the Conversation tab, **click the "Merge pull request" button** (near the bottom
    of the page)

- If the submission failed to meet all of the criteria in the above rubric:

  - In the "Leave a comment" section:

    - Tag the submitter (e.g. ``@natcap-bot``)
    - Paste the review rubric and check the boxes for the criteria that have been met
      (by placing an ``x`` between the brackets, e.g. ``[x]``)
    - Write an explanation of the missing / unmet criteria
    - Include the following instructions for the submitter: "Please review the above
      comments and address them accordingly in this PR. Please do not close this PR and
      open a new one."

  - Select the "Request changes" radio button
  - Click the green "Submit review" button
