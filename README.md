# Software Templates

A set of sample software templates.


# Changes from base template 

* Update the template.yaml under deploy-component dir with your own orgid in the repo url such as repoUrl: github.com?repo=app-of-apps&owner=rh-product-demos
* Make sure there is a catalog-info.yaml under crewai/skeleton that has source location with your orgname . Eg: backstage.io/source-location: url:https://github.com/rh-product-demos/${{ values.name }}
* Description of application and application name should be updated in chart.yaml for both production and deployment folders
* template.yaml under your app folder should be using your orgid for repoURL
* Values.yaml be updaed with your software template name instead of base template 
* In template.yaml under deployment-yaml make sure it is  `namespace: openshift-gitops`