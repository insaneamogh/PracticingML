
invokeAgentforce() {
    this.submitSuccess = false;
    this.submitError = undefined;
    this.createdRecordLabel = undefined;
    this.createdRecordId = undefined;
    this.isLoading = true;

    // Reset UI states
    this.showNoRecommendations = false;
    this.response = null;
    this.actionReviews = [];
    this.showReviewScreen = false;

    askAgentInvocable({
        taskId: this.recordId,
        prompt: this.description,
        agent: 'Advisor_Agent'
    })
    .then(res => {
        let parsedObj = res;

        // Safely parse if response is a string (common with Agentforce)
        if (typeof parsedObj === 'string') {
            try {
                parsedObj = JSON.parse(parsedObj);
            } catch (e) {
                this.response = errorParseAgent;
                this.isLoading = false;
                console.error('JSON Parse Error:', e);
                return;
            }
        }

        const aiResponse = parsedObj?.value;

        // CHECK FOR NO ACTIONS / EMPTY RESPONSE
        const hasActions = aiResponse && (
            (Array.isArray(aiResponse) && aiResponse.length > 0) ||
            (aiResponse.actions && Array.isArray(aiResponse.actions) && aiResponse.actions.length > 0) ||
            (typeof aiResponse === 'object' && Object.keys(aiResponse).length > 0) ||
            (typeof aiResponse === 'string' && aiResponse.trim() !== '')
        );

        if (!hasActions) {
            // NO ACTIONS → Show friendly message
            this.showNoRecommendations = true;
            this.isLoading = false;
            return; // Skip fetching reviews — nothing to show
        }

        // HAS ACTIONS → Store and proceed
        this.response = aiResponse;
        this.showNoRecommendations = false;

        console.log('Agentforce Response:', this.response);

        // Now fetch any existing reviews (optional but good UX)
        return getMeetingNoteActionReviewDetails({ taskId: this.recordId });
    })
    .then(async result => {
        if (result) {
            this.actionReviews = await Promise.all((result || []).map(async ar => ({
                ...ar,
                fields: await this.decorateFieldsForDisplay(ar.fields)
            })));
        }
        this.showReviewScreen = true;
        this.isLoading = false;
    })
    .catch(err => {
        // Any error in agent call OR review fetch
        this.isLoading = false;
        this.showNoRecommendations = false;
        this.response = null;

        const errorMsg = err?.body?.message || err?.message || err;
        this.response = errorAgentFailed + (errorMsg ? ` ${errorMsg}` : '');

        console.error('Agentforce or Review Fetch Failed:', err);
    });
}
