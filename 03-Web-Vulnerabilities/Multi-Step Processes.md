### Access Control in Multi-Step Processes

#### Idea

Some sensitive operations are split into multiple steps.

Example:

1. Load edit form
2. Submit changes
3. Confirm changes

#### Vulnerability

The application protects the first steps but forgets to enforce authorization on the final step.

It assumes that anyone reaching the last step has already passed the previous authorized steps.

An attacker can bypass the workflow and send the final request directly.

#### Root Cause

- Trusting the application workflow.
- Missing authorization checks on every sensitive request.

#### Exploitation

1. Complete the workflow once.
2. Capture all requests with Burp.
3. Identify the final action request.
4. Replay the final request directly.
5. Check whether the action is performed without proper authorization.

#### Remember

Every sensitive endpoint must perform its own authorization check, regardless of how the user reached it.