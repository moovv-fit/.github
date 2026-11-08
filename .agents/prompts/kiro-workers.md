# TASK: Provision Kiro Multi-Worker Identities \& Credential Store via AWS CDK

## Objective

Implement an infrastructure stack in our existing AWS CDK repository (`repos/infra/cdk` or equivalent infra package) to manage automated Kiro worker identities. The stack must provision an IAM Identity Center (AWS SSO) Group, two worker users, assign group memberships, and scaffold SSM Parameter Store SecureString placeholders for headless Kiro API keys (`ksk\_...`).

Do not hardcode sensitive tokens or IDs. Follow AWS Well-Architected and CDK TypeScript best practices.

\---

## 1\. Context \& Architectural Requirements

1. **Target Architecture:**

   * **Service Layer:** AWS IAM Identity Center via L1 CloudFormation constructs (`aws-cdk-lib/aws-identitystore`).
   * **Secret Storage:** AWS Systems Manager Parameter Store (`aws-cdk-lib/aws-ssm`).
   * **Worker Pool:** Provision 2 worker identities (`worker-1`, `worker-2`) intended for headless CLI runs and parallel Spot runners.
   * **Billing Alignment:** The provisioned group will be bound to our existing AWS-managed Kiro subscription, drawing directly from our AWS account credits (AWS Activate).
2. **Naming \& Hierarchy Invariants:**

   * **Stack Name:** `moovv-fit-platform-kiro-identity-{environment}`
   * **Worker Group Display Name:** `moovv-kiro-workers-{environment}`
   * **User Naming Pattern:**

     * `userName`: `kiro-{workerId}-{environment}@moovv.fit`
     * `displayName`: `Kiro Worker {workerId} ({environment})`
     * `primaryEmail`: `tech+kiro-{workerId}@moovv.fit`
   * **SSM Parameter Naming Pattern:**

     * `/moovv-fit/kiro/accounts/{workerId}/api-key`
     * Type: `StringParameter` (with instructions/scripts to overwrite as `SecureString` once keys are generated).

\---

## 2\. Implementation Instructions

### Step 1: Pre-flight Audit

1. Inspect `package.json` in the infra repository. Ensure `aws-cdk-lib` (v2.x) and `constructs` (v10.x) are available.
2. Locate existing environment configurations (e.g., `lib/config/environments.ts`) and CDK app entry point (`bin/app.ts`).
3. Identify how the `identityStoreId` (e.g., `d-xxxxxxxxxx`) is passed (via CDK Context, SSM Parameter lookup, or environment configuration).

### Step 2: Implement `KiroWorkerIdentityStack`

Create `lib/stacks/kiro-worker-identity-stack.ts` (or place under the appropriate stack directory):

```typescript
import \* as cdk from 'aws-cdk-lib';
import \* as identitystore from 'aws-cdk-lib/aws-identitystore';
import \* as ssm from 'aws-cdk-lib/aws-ssm';
import { Construct } from 'constructs';

export interface KiroWorkerIdentityStackProps extends cdk.StackProps {
  /\*\*
   \* The Identity Store ID from AWS IAM Identity Center (e.g. d-1234567890).
   \*/
  readonly identityStoreId: string;

  /\*\*
   \* Deployment environment name ('staging' | 'production').
   \*/
  readonly environment: string;

  /\*\*
   \* Worker identifiers to provision.
   \* @default \['worker-1', 'worker-2']
   \*/
  readonly workerIds?: string\[];
}

export class KiroWorkerIdentityStack extends cdk.Stack {
  public readonly workerGroup: identitystore.CfnGroup;

  constructor(scope: Construct, id: string, props: KiroWorkerIdentityStackProps) {
    super(scope, id, props);

    const { identityStoreId, environment, workerIds = \['worker-1', 'worker-2'] } = props;

    // 1. Group to hold Kiro workers (for bulk subscription attachment in Kiro Console)
    this.workerGroup = new identitystore.CfnGroup(this, 'KiroWorkersGroup', {
      identityStoreId,
      displayName: `moovv-kiro-workers-${environment}`,
      description: `Automated headless Kiro CLI workers for ${environment}`,
    });

    // 2. Iterate and create worker users, memberships, and SSM parameter placeholders
    workerIds.forEach((workerId) => {
      const user = new identitystore.CfnUser(this, `KiroUser-${workerId}`, {
        identityStoreId,
        userName: `kiro-${workerId}-${environment}@moovv.fit`,
        displayName: `Kiro Worker ${workerId} (${environment})`,
        name: {
          givenName: 'Kiro',
          familyName: workerId,
        },
        emails: \[
          {
            value: `tech+kiro-${workerId}@moovv.fit`,
            primary: true,
            type: 'work',
          },
        ],
      });

      // Bind user to the worker group
      new identitystore.CfnGroupMembership(this, `KiroMembership-${workerId}`, {
        identityStoreId,
        groupId: this.workerGroup.attrGroupId,
        memberId: {
          userId: user.attrUserId,
        },
      });

      // SSM parameter placeholder for headless Kiro API keys
      new ssm.StringParameter(this, `KiroApiKeyParam-${workerId}`, {
        parameterName: `/moovv-fit/kiro/accounts/${workerId}/api-key`,
        description: `API key for headless Kiro spot worker ${workerId} (${environment})`,
        stringValue: 'placeholder-populate-via-cli',
        tier: ssm.ParameterTier.STANDARD,
      });
    });

    // 3. Stack Outputs for easy console lookup and downstream automation
    new cdk.CfnOutput(this, 'KiroWorkerGroupId', {
      value: this.workerGroup.attrGroupId,
      description: 'IAM Identity Center Group ID to subscribe in Kiro Console',
      exportName: `moovv-fit-kiro-worker-group-id-${environment}`,
    });

    new cdk.CfnOutput(this, 'IdentityStoreIdOutput', {
      value: identityStoreId,
      description: 'IAM Identity Center Store ID used for deployment',
    });
  }
}



Step 3: Wire into App Entrypoint

In bin/app.ts:



Import KiroWorkerIdentityStack.



Retrieve identityStoreId either from CDK context (app.node.tryGetContext('identityStoreId')) or environment config.



Instantiate the stack for staging (and optionally production).



Apply standard tags:



project: moovv-fit



service: kiro-runner



managedBy: cdk



Step 4: Verification \& Quality Gates

Run pnpm check / pnpm lint to ensure formatting matches Biome / ESLint rules.



Run pnpm type-check to verify TypeScript compilation.



Run pnpm cdk synth moovv-fit-platform-kiro-identity-staging and inspect synthesized CloudFormation template to verify:



Resource types AWS::IdentityStore::Group, AWS::IdentityStore::User, and AWS::IdentityStore::GroupMembership are rendered correctly.



Outputs include KiroWorkerGroupId.



3\. Required Deliverable Summary

Upon completing the code changes, generate a concise summary containing:



List of files modified or created.



The exact CDK CLI commands to synth and deploy the stack.



The post-deployment runbook commands for:



Getting the identityStoreId via AWS CLI if missing (aws sso-admin list-instances).



One-time AWS Console action to attach the new group to the Kiro subscription.



The AWS CLI aws ssm put-parameter command to overwrite the placeholder with the real ksk\_... API key.





\*\*\*



\### Recommended Manual Checklist

After Kiro generates and deploys the stack, complete these one-time steps:



1\. \*\*Verify your Identity Store ID:\*\*

&#x20;  ```bash

&#x20;  aws sso-admin list-instances --region ap-south-1 --query "Instances\[0].IdentityStoreId" --output text

Assign Group to Kiro Subscription:



Go to AWS Console > Kiro > Users \& Groups > Groups tab.



Click Add group, select moovv-kiro-workers-staging, and select your desired plan (Pro tier or Credit Sharing).



Save Generated Keys to SSM:



Bash

aws ssm put-parameter \\

&#x20; --name "/moovv-fit/kiro/accounts/worker-1/api-key" \\

&#x20; --value "ksk\_your\_actual\_key" \\

&#x20; --type "SecureString" \\

&#x20; --overwrite \\

&#x20; --region ap-south-1

