import { LightningElement, api, wire, track } from 'lwc';
import askAgentInvocable from '@salesforce/apex/AF_AgentInvocationService.AF_InvokeAgent';
import getMeetingNoteActionReviewDetails from '@salesforce/apex/AF_MeetingNoteActionHandler.getMeetingNoteActionReviewDetails';
import getUserNameById from '@salesforce/apex/AF_TaskManageAction.getUserNameById';
import getTask from '@salesforce/apex/AF_TaskDataController.getTask';
import { subscribe } from 'lightning/empApi';
import { refreshApex } from '@salesforce/apex';
import runAction from '@salesforce/apex/AF_MeetingNoteActionRunner.runAction';
import { ShowToastEvent } from 'lightning/platformShowToastEvent';

import cardTitle from '@salesforce/label/c.af_card_title';
import pageIntro from '@salesforce/label/c.af_page_intro';
import createFollowup from '@salesforce/label/c.af_create_followup_button';
import reviewTitle from '@salesforce/label/c.af_review_title';
import submitLabel from '@salesforce/label/c.af_submit';
import successHeadingLabel from '@salesforce/label/c.af_success_heading';
import successLink from '@salesforce/label/c.af_success_link';
import errorParseAgent from '@salesforce/label/c.af_error_parse_agent';
import noRecommendationTitle from '@salesforce/label/c.af_no_recommendation_title';
import noRecommendation from '@salesforce/label/c.af_no_recommendation';
import errorAgentFailed from '@salesforce/label/c.af_error_agent_failed';

export default class AFAgentforceFollowUpActions extends LightningElement {
    @api recordId;
    @track task;
    @track error;
    description = '';
    response;
    @api channelName = '/event/Task_Updated__e';
    @track isLoading = false;
    wiredTaskData;

    @track actionReviews = [];
    @track showReviewScreen = false;
    @track showNoRecommendations = false;
    @track createdRecordLabel;
    @track createdRecordId;
    @track submitSuccess = false;
    @track submitError;

    // Custom Labels
    cardTitle = cardTitle;
    pageIntro = pageIntro;
    createFollowup = createFollowup;
    reviewTitle = reviewTitle;
    submitLabel = submitLabel;
    successLink = successLink;
    noRecommendationTitle = noRecommendationTitle;
    noRecommendation = noRecommendation;
    errorParseAgent = errorParseAgent;
    errorAgentFailed = errorAgentFailed;

    get successHeading() {
        return successHeadingLabel.replace('{0}', this.createdRecordLabel || '');
    }

    get createdRecordUrl() {
        return this.createdRecordId ? `/${this.createdRecordId}` : '#';
    }

    @wire(getTask, { recordId: '$recordId', description : '$description' })
    wiredTask({ error, data }) {
        this.wiredTaskData = data;
        if (data) {
            this.task = data;
            this.description = data.Description || '';
        } else if (error) {
            this.error = error;
        }
    }

    // Helper: Converts YYYY-MM-DD to MM-DD-YYYY
    formatDateForDisplay(val) {
        if (!val) return '';
        if (/^\d{4}-\d{2}-\d{2}$/.test(val)) {
            const [year, month, day] = val.split('-');
            return `${month}-${day}-${year}`;
        }
        return val;
    }

    // Decorate each field: add .uiValue for easy template display
    async decorateFieldsForDisplay(fields) {
        return Promise.all(fields.map(async f => {
            const field = { ...f };
            // Optionally replace OwnerId with user name
            if (field.name === 'OwnerId' && field.value) {
                field.name = 'Assigned To';
                try {
                    const userName = await getUserNameById({ userId: field.value });
                    field.value = userName;
                } catch (e) { /* ignore */ }
            }
            // If it's a date type or field name/label has 'date', format it
            if (
                (field.type && field.type.toLowerCase() === 'date') ||
                (field.apiName && field.apiName.toLowerCase().includes('date')) ||
                (field.label && field.label.toLowerCase().includes('date'))
            ) {                
                field.displayValue = this.formatDateForDisplay(field.value);
            }
            // Always set .uiValue to display in template
            field.uiValue = field.displayValue || field.value;
            return field;
        }));
    }

    async invokeAgentforce() {
        this.submitSuccess = false;
        this.submitError = undefined;
        this.createdRecordLabel = undefined;
        this.createdRecordId = undefined;
        this.showReviewScreen = false;
        this.showNoRecommendations = false;
        this.isLoading = true;

        try {
            // Force refresh the wired data first (mimic hard refresh)
            await refreshApex(this.wiredTaskData);
            
            // Get absolutely fresh task data - bypass any caching
            const taskData = await getTask({ recordId: this.recordId, description: null });
            const currentDescription = taskData?.Description || '';
            
            // Update local description with fresh data
            this.description = currentDescription;
            
            // Validate if description/prompt exists
            if (!currentDescription || currentDescription.trim() === '') {
                this.isLoading = false;
                this.actionReviews = [];
                this.showReviewScreen = false;
                this.showNoRecommendations = true;
                return;
            }

            // Call agent with current description
            const agentResponse = await askAgentInvocable({ taskId: this.recordId, prompt: currentDescription });
            
            let parsedObj = agentResponse;
            if (typeof parsedObj === 'string') {
                try {
                    parsedObj = JSON.parse(parsedObj);
                } catch (e) {
                    this.response = this.errorParseAgent || 'Agentforce response could not be parsed.';
                    this.isLoading = false;
                    this.showReviewScreen = false;
                    this.showNoRecommendations = false;
                    return;
                }
            }
            this.response = parsedObj && parsedObj.value ? parsedObj.value : 'Agent did not respond as expected.';

            // Get review details
            const result = await getMeetingNoteActionReviewDetails({ taskId: this.recordId });
            
            if (result && result.length > 0) {
                this.actionReviews = await Promise.all(result.map(async ar => ({
                    ...ar,
                    fields: await this.decorateFieldsForDisplay(ar.fields)
                })));
                this.showReviewScreen = true;
                this.showNoRecommendations = false;
            } else {
                this.actionReviews = [];
                this.showReviewScreen = false;
                this.showNoRecommendations = true;
            }
            
        } catch (err) {
            this.response = this.errorAgentFailed || 'Failed to fetch review details or Agentforce call failed: ' + (err.body?.message || err.message || err);
            this.showReviewScreen = false;
            this.showNoRecommendations = false;
            console.error('Error in invokeAgentforce:', err);
        } finally {
            this.isLoading = false;
        }
    }

    // This method is called on click of submit button
    async handleSubmit(event) {
        const idx = event.target.dataset.index;
        const actionReview = this.actionReviews[idx];
        if (!actionReview) return;

        const fields = {};
        actionReview.fields.forEach(fld => {
            fields[fld.apiName] = fld.value !== '' && fld.value !== undefined ? fld.value : null;
        });

        const objectApiName = actionReview.action.AF_Object_Name__c;
        const actionId = actionReview.action.id;
        this.submitError = undefined;
        this.isLoading = true;

        try {
            const result = await runAction({
                objectApiName: objectApiName,
                fieldValues: fields,
                taskId: this.recordId,
                actionId: actionId
            });

            if (result.errorMessage) {
                this.submitError = result.errorMessage;
                this.submitSuccess = false;
            } else {
                this.createdRecordLabel = result.objectLabel;
                this.createdRecordId = result.recordId;
                this.submitSuccess = true;

                // Show sticky toast notification at the top
                const toastEvent = new ShowToastEvent({
                    title: 'Success!',
                    message: `${this.createdRecordLabel} has been created. {0}`,
                    messageData: [
                        {
                            url: this.createdRecordUrl,
                            label: `View ${this.createdRecordLabel}`
                        }
                    ],
                    variant: 'success',
                    mode: 'sticky'
                });
                this.dispatchEvent(toastEvent);
            }

        } catch (error) {
            this.submitError = error.body ? error.body.message : error.message;
            this.submitSuccess = false;
        }

        this.isLoading = false;
    }

    connectedCallback() {
        subscribe(this.channelName, -1, () => { this.refreshMyData(); })
            .then(response => { })
            .catch(err => { });
    }
    
    refreshMyData(){
        refreshApex(this.wiredTaskData).then(() =>{});
    }
}

