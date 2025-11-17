# PracticingML
public with sharing class AF_MeetingNoteActionRunner {
   
        public static final String OPPORTUNITY = 'Opportunity';
        public static final String OWNER_ID = 'OwnerId';
        public static final String STAGE_NAME = 'StageName';
        public static final String STAGE_PRE_DISCOVERY = 'Pre-Discovery';
        public static final String LEGACY_ID = 'AF_Legacy_ID__c';
        public static final String LEGACY_ID_VAL = 'Agentforce';
        public static final String LEAD_SOURCE = 'LeadSource';
        public static final String LEAD_SOURCE_OTHER = 'Other';
        public static final String CLOSE_DATE = 'CloseDate';

        public static final String TASK = 'Task';
        public static final String RECORD_TYPE_ID = 'RecordTypeId';
        public static final String TASK_DEV_NAME = 'Advisory_Task';
        public static final String TYPE = 'Type';
        public static final String TYPE_TODO = 'To Do';
        public static final String STATUS = 'Status';
        public static final String STATUS_NOT_STARTED = 'Not Started';
        public static final String WHAT_ID = 'WhatId';
        public static final String WHO_ID = 'WhoId';
 

    @AuraEnabled
    public static Map<String, Object> runAction(String objectApiName, Map<String, Object> fieldValues, String taskId, String actionId) {
        Map<String, Object> result = new Map<String, Object>();
        try {
            SObjectType sobjectType = Schema.getGlobalDescribe().get(objectApiName);
            SObject newObj = sobjectType.newSObject();
            Map<String, SObjectField> fieldMap = sobjectType.getDescribe().fields.getMap();

            populateSObjectFields(newObj, fieldMap, fieldValues);

            /*if (objectApiName == OPPORTUNITY) {
                setOpportunityDefaults(newObj, fieldMap, fieldValues);
            } else if (objectApiName == TASK) {
                setTaskDefaults(newObj, fieldMap, fieldValues, taskId);
            }*/

            insert newObj;
            result.put('objectLabel', sobjectType.getDescribe().getLabel());
            result.put('recordId', newObj.Id);
            result.put('errorMessage', null);

            if (! String.isBlank(actionId)) {
                cleanupActionAndChildren(actionId, result);
            }
        } catch (Exception e) {
            result.put('objectLabel', null);
            result.put('recordId', null);
            result.put('errorMessage', e.getMessage());
        }
        return result;
    }

    // Populates SObject fields per provided map and converts types appropriately
    private static void populateSObjectFields(SObject newObj, Map<String, SObjectField> fieldMap, Map<String, Object> fieldValues) {
        for (String field : fieldValues.keySet()) {
            Object val = fieldValues.get(field);
            if (!fieldMap.containsKey(field)) {
                continue;
            }
            Schema.DisplayType type = fieldMap.get(field).getDescribe().getType();
            if (val != null) {
                switch on type {
                    when DATE {
                        if (val instanceof String) {
                            newObj.put(field, Date.valueOf((String)val));
                        } else {
                            newObj.put(field, val);
                        }
                    }
                    when DATETIME {
                        if (val instanceof String) {
                            newObj.put(field, DateTime.valueOf((String)val));
                        } else {
                            newObj.put(field, val);
                        }
                    }
                    when BOOLEAN {
                        if (val instanceof String) {
                            newObj.put(field, ((String)val).toLowerCase() == 'true');
                        } else if (val instanceof Boolean) {
                            newObj.put(field, val);
                        }
                    }
                    when INTEGER, DOUBLE, CURRENCY, PERCENT {
                        if (val instanceof String) {
                            newObj.put(field, Decimal.valueOf((String)val));
                        } else {
                            newObj.put(field, val);
                        }
                    }
                    when else {
                        newObj.put(field, val);
                    }
                }
            }
        }
    }

    // Sets Opportunity-specific defaults
   /* private static void setOpportunityDefaults(SObject newObj, Map<String, SObjectField> fieldMap, Map<String, Object> fieldValues) {
        if (!fieldValues.containsKey( OWNER_ID) && fieldMap.containsKey( OWNER_ID)) {
            newObj.put( OWNER_ID, UserInfo.getUserId());
        }
        if (!fieldValues.containsKey(STAGE_NAME) && fieldMap.containsKey(STAGE_NAME)) {
            newObj.put(STAGE_NAME, STAGE_PRE_DISCOVERY);
        }
        if (!fieldValues.containsKey(LEGACY_ID) && fieldMap.containsKey(LEGACY_ID)) {
            newObj.put(LEGACY_ID, LEGACY_ID_VAL);
        }
        if (!fieldValues.containsKey(LEAD_SOURCE) && fieldMap.containsKey(LEAD_SOURCE)) {
            newObj.put(LEAD_SOURCE, LEAD_SOURCE_OTHER);
        }
         System.debug('Checking close date conditions: fieldValues.containsKey=' + fieldValues.containsKey(CLOSE_DATE) + 
                 ', fieldValues.get=' + fieldValues.get(CLOSE_DATE) +
                 ', fieldMap.containsKey=' + fieldMap.containsKey(CLOSE_DATE));
        if ((!fieldValues.containsKey(CLOSE_DATE) || fieldValues.get(CLOSE_DATE) == null)
            && fieldMap.containsKey(CLOSE_DATE)
        ) {
             Date defaultCloseDate = Date.today().addDays(90);
            newObj.put(CLOSE_DATE, defaultCloseDate);
            System.debug('Defaulting close date to ' + defaultCloseDate);
        }else{
        System.debug('Not defaulting close date');
        }
    }*/

    // Sets Task-specific defaults and copies WhatId/WhoId from source if taskId provided
    private static void setTaskDefaults(SObject newObj, Map<String, SObjectField> fieldMap, Map<String, Object> fieldValues, String taskId) {
        if (!fieldValues.containsKey(RECORD_TYPE_ID) && fieldMap.containsKey(RECORD_TYPE_ID)) {
            RecordType rt = [SELECT Id FROM RecordType WHERE SObjectType = :TASK AND DeveloperName = :TASK_DEV_NAME LIMIT 1];
            newObj.put(RECORD_TYPE_ID, rt.Id);
        }
        /*if (!fieldValues.containsKey(TYPE) && fieldMap.containsKey(TYPE)) {
            newObj.put(TYPE, TYPE_TODO);
        }
        if (!fieldValues.containsKey(STATUS) && fieldMap.containsKey(STATUS)) {
            newObj.put(STATUS, STATUS_NOT_STARTED);
        }*/

        if (String.isNotBlank(taskId)) {
            try {
                Task origTask = [SELECT WhatId, WhoId FROM Task WHERE Id = :taskId LIMIT 1];
                if (!fieldValues.containsKey(WHAT_ID) && fieldMap.containsKey(WHAT_ID) && origTask.WhatId != null) {
                    newObj.put(WHAT_ID, origTask.WhatId);
                }
                if (!fieldValues.containsKey(WHO_ID) && fieldMap.containsKey(WHO_ID) && origTask.WhoId != null) {
                    newObj.put(WHO_ID, origTask.WhoId);
                }
            } catch (Exception ex) {
                System.debug(LoggingLevel.ERROR, 'Error retrieving original task: ' + ex.getMessage());            }
        }
    }

    // Cleans up actions and children, with error handling
    private static void cleanupActionAndChildren(String actionId, Map<String, Object> result) {
        try {
            List<AF_Meeting_Note_Action_Data__c> childrenToDelete = [
                SELECT Id FROM AF_Meeting_Note_Action_Data__c WHERE AF_Meeting_Note_Action__c = :actionId
            ];
            if (!childrenToDelete.isEmpty()) {
                delete childrenToDelete;
            }
            AF_Meeting_Note_Action__c actionToDelete = [
                SELECT Id FROM AF_Meeting_Note_Action__c WHERE Id = :actionId LIMIT 1
            ];
            delete actionToDelete;
        } catch (Exception deleteEx) {
            result.put('deleteWarning', deleteEx.getMessage());
        }
    }
}
