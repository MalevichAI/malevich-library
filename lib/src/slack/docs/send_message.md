# Send Message to Slack

## General Component Purpose

The "Send Message to Slack" component is designed to facilitate communication within Slack directly from our no-code platform. It enables users to send messages to specified Slack channels by providing a simple interface to input the necessary information. This component is ideal for automating notifications, alerts, or updates to your team's Slack channels as part of your product pipeline.

## Input and Output Format

### Input Format

The input for this component is a tabular data format that must include the following columns:

- `channel_id`: The ID of the Slack channel where the message will be sent.
- `message`: The content of the message to be sent to the channel.

Each row in the table represents a separate message to be sent to a Slack channel.

### Output Format

The output of this component is also a tabular data format with the following columns:

- `channel_id`: The ID of the Slack channel to which the message was sent.
- `message`: The content of the message that was sent to the channel.

The output confirms the messages that have been dispatched to their respective channels.

## Configuration Parameters

| Parameter | Type   | Description      |
|-----------|--------|------------------|
| token     | String | Slack token used for authentication to send messages to the specified Slack channel. |

## Configuration Parameters Details

- **token**: This is the Slack API token that is required for the component to authenticate with Slack and send messages to the channels. The token should have the necessary permissions to post messages to the specified channels.

## Usage

To use this component, ensure that you have a valid Slack token and that your input data is formatted correctly with the required `channel_id` and `message` columns. Once configured, the component will send each message to the corresponding Slack channel and return a confirmation of the messages sent. This can be used to verify successful communication or to log activity within your pipeline.