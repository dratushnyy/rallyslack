# CA Agile Rally integration with Slack messenger
  - More about [Rally]
  - More about [Slack]

## Requirements
  - [Custom integration for slack]
  - [Rally] account
  - [Rally application]
  - Some server to host the code
  - Valid SSL certificate
         Since Slack demand to use ssl connection, there are two options to do it:
         Use CA signed certificate.
         [CloudFlare] certificate for connection between Slack and your host and self-signed certificate for connection between CloudFlare and your host

# Supported commands in Slack
    - /rally us[all] - list userstories
   
 
[Rally]: <http://rallydev.com>
[Slack]: <http://slack.com>
[Custom integration for slack]: https://api.slack.com/custom-integrations
[Rally application]: https://help.rallydev.com/rally-application-manager
[CloudFlare]: https://www.cloudflare.com/
