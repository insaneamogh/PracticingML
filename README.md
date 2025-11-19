@isTest
private class AF_MeetingNoteActionRunner_Test {

@isTest
static void testRunActionAndCleanup_Task() {

// Create temp action record
AF_Meeting_Note_Action__c tempAction = new AF_Meeting_Note_Action__c(
Name = 'Test Temp Action',
AF_Status__c = 'Pending'
);
insert tempAction;

// Prepare fieldValues required to create Task
Map<String, Object> fieldValues = new Map<String, Object>{
'Subject' => 'Follow-up Task',
'Status' => 'Not Started'
};

Test.startTest();
Map<String, Object> result = AF_MeetingNoteActionRunner.runAction(
'Task',
fieldValues,
null,
tempAction.Id
);
Test.stopTest();

String createdRecordId = (String) result.get('recordId');
System.assertNotEquals(null, createdRecordId);

// Validate task created
Task t = [SELECT Id, Subject FROM Task WHERE Id = :createdRecordId LIMIT 1];
System.assertEquals('Follow-up Task', t.Subject);

// Validate cleanup updates
AF_Meeting_Note_Action__c updatedAction = [
SELECT AF_Status__c, AF_Created_Follow_Up_Action__c, AF_Type__c
FROM AF_Meeting_Note_Action__c
WHERE Id = :tempAction.Id
LIMIT 1
];

System.assertEquals('Saved Successfully', updatedAction.AF_Status__c);
System.assertEquals(createdRecordId, updatedAction.AF_Created_Follow_Up_Action__c);
System.assertEquals('Task', updatedAction.AF_Type__c); // REQUIRED
}
}
