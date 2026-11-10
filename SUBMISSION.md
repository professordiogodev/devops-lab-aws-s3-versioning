# Submission

Fork URL: <!-- paste the URL of your fork here -->

## Files to commit

- [ ] `notes.md` with your commands and what you saw (optional)

## Questions

Answer in your own words. Where a question asks for output, paste it in a code block.

### Q1. After the first `./incident.sh` (no versioning), paste the proof that the report and the customer list could not be recovered. What would have saved them?

**Your answer:**

<!-- replace this line with your answer -->

### Q2. After the second incident, paste `aws s3api list-object-versions` for both files. What is a delete marker and why does a deleted file still exist?

**Your answer:**

<!-- replace this line with your answer -->

### Q3. Show the exact commands that restored the report and the customer list. Why restore by copying the old version to the current key instead of deleting the newest version?

**Your answer:**

<!-- replace this line with your answer -->

### Q4. Paste your lifecycle rules. After one year, what happens to the old versions and to the incomplete multipart uploads, and what would the bucket cost without them?

**Your answer:**

<!-- replace this line with your answer -->

### Q5. Default encryption is on (SSE-S3). When would you use SSE-KMS with your own key instead, and what extra failure can it introduce?

**Your answer:**

<!-- replace this line with your answer -->

### Q6. Paste the output of `./verify.sh`. It must end with **ALL CHECKS PASSED**.

**Your answer:**

<!-- replace this line with your answer -->

### Q7. **Tear down.** Paste the output of `./verify-teardown.sh`. It must end with **TEARDOWN VERIFIED**.

**Your answer:**

<!-- replace this line with your answer -->
