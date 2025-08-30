# Auth0 Security Detection Catalog

[![Blog](https://img.shields.io/badge/blog-okta_security-blue)][secblog]
[![Advisories](https://img.shields.io/badge/advisories-okta_security_advisories-blue)][advisories]
[![EventTypes](https://img.shields.io/badge/docs-auth0_event_types-blue)][eventtypes]

Welcome to the Auth0 Security Detection Catalog. This repository contains a collection of detection rules for security monitoring of Auth0 environments. New detections will be added to this catalogue routinely.

## Who We Are

Okta Identity Defense Operations is a team of security practitioners that help Okta and Auth0 customers investigate and respond to security incidents. If you are an Okta/Auth0 customer and need support with a security breach or incident, open a support case and indicate that you are investigating a security incident.

## Getting Started

Auth0 [logs](https://auth0.com/docs/deploy-monitor/logs) provide detailed user, admin and support events relevant to use of the Auth0 tenant.

These events can be [browsed, searched or filtered in the admin Auth0 Dashboard](https://auth0.com/docs/deploy-monitor/logs/view-log-events). They can also be queried and filtered programmatically via the [Logs API](https://auth0.com/docs/api/management/v2/logs/get-logs). [Auth0 documentation](https://auth0.com/docs/secure/security-guidance/incident-response-using-logs) provides some basic guidance on how to work with logs through Auth0 Dashboard.

Each log entry is attributed with an [event type](https://auth0.com/docs/customize/events/event-types). Some attributes are searchable with the [Lucene Syntax](https://auth0.com/docs/deploy-monitor/logs/log-search-query-syntax).

Okta Security recommends the use of [Log Streaming](https://auth0.com/docs/customize/log-streams) to capture events in third-party security tools in close to real-time and/or the use of [Auth0 Actions](https://auth0.com/docs/customize/actions) for security orchestration opportunities. Besides extended retention ([your Auth0 log data retention period depends on your subscription level](https://auth0.com/docs/deploy-monitor/logs/log-data-retention)), this will allow security teams to conduct a more sophisticated search and analysis of logs.

Most of the detections provided in this catalogue require logs to be streamed to the third-party tools, e.g. Splunk. However, each detection is also attributed with a query in the Lucene syntax that can be used directly in the Auth0 Dashboard. This will help to locate log entries of interest, while further analysis should be conducted with the third-party tool.

## Schema and compatibility {schema}

The detection rules in the `detections/` directory are compatible with the [Sigma](https://sigmahq.io/) rule specification [v2.0.0](https://github.com/SigmaHQ/sigma-specification/blob/3e27a92ca649c2798e65b4300bf58deee1149118/json-schema/sigma-detection-rule-schema.json). As a convenience for users, we have included arbirary custom fields that provide more detailed examples as an aid for users.

### Custom Fields

The table below lists the custom fields we have added in addition to the fields required by the Sigma rule specification.

| Field Name    | Description                                                                    |
|---------------|--------------------------------------------------------------------------------|
| `tenant_logs` | Raw [Auth0 log queries](https://auth0.com/docs/deploy-monitor/logs)            |
| `prevention`  | Human-readable suggestions on how to prevent the attack in the detection rule  |
| `explanation` | Human-readable long-form explanation of the Splunk query                       |
| `splunk`      | Highly-detailed example Splunk query beyond what Sigma automatically generates |
| `comments`    | Additional information on the rule                                             |

## Using Detection Rules with Sigma CLI

You can use the [Sigma CLI](https://github.com/SigmaHQ/sigma-cli) tool to convert these rules into queries for your specific SIEM platform.

### Installation

Install the Sigma CLI following the official [`sigma-cli` documentation](https://github.com/SigmaHQ/sigma-cli?tab=readme-ov-file#getting-started).

### Converting Detection Rules

To convert a detection rule to your target platform, use:

```bash
sigma convert --target <target> detections/<rule-file>.yml
```

### Example

Convert the brute force detection rule to Datadog format:

```bash
$ sigma convert \                                    
    --target datadog \
    detections/unrecognized_ip_in_allowlist.yml
```

```
Parsing Sigma rules  [####################################]  100%
(@source:auth0 AND @type:sapi AND @tenant_name:* AND (@description:Update\ Brute\-force\ settings OR @description:Create\ or\ update\ the\ anomaly\ detection\ captcha OR @description:Update\ Suspicious\ IP\ Throttling\ settings)) AND (NOT @request.body.allowlist:192.0.2.0/24)
```

This will output a Datadog search query that you can use directly in your environment to detect brute force attacks against Auth0 authentication endpoints.

## Using Detection Rules with other automation tools

Our [additional fields](#schema) allow you to easily parse the provided YAML files and drop in your favorite tool programatically. For example, you could parse a rule like so and use it in Splunk's official SDK.

```python
In [1]: import yaml

In [2]: with open('detections/breached_password_detection_settings_manipulated.yml', 'r') as f:
   ...:     detection = yaml.safe_load(f)
   ...:

In [3]: print(detection['splunk'].strip())
index=auth0 data.tenant_name="{your-tenant-name}"
data.type=sapi data.description="Update Breached Password Detection settings"
``` Excluding white-listed IPs```
``` NOT data.ip IN ("{white-listed-IPs}")```
```Take only the last change of configurations that reflects the current settings```
| sort - _time
| head 1
| rename data.details.response.body.shields{} as login_shields
| rename data.details.response.body.enabled as breached_protection_enabled
| rename data.details.response.body.stage.pre-user-registration.shields{} as signup_shields
| eval user_notifications_on = if(isnotnull(mvfind(login_shields, "user_notification")), "true", "false")
| eval login_flow_is_protected = if(isnotnull(mvfind(login_shields, "block")), "true", "false")
| eval signup_flow_is_protected = if(isnotnull(mvfind(signup_shields, "block")), "true", "false")
```Alert when breached password protection is completely disabled or all responses are disabled (login, signup). Note: pwd reset is masked by now.```
| where breached_protection_enabled = "false" OR (login_flow_is_protected = "false" AND signup_flow_is_protected = "false")
```Display the information in a table```
| table _time, data.ip, breached_protection_enabled, login_flow_is_protected, signup_flow_is_protected, user_notifications_on
```

[secblog]: https://sec.okta.com/articles
[advisories]: https://trust.okta.com/security-advisories/
[eventtypes]: https://auth0.com/docs/customize/events/event-types
