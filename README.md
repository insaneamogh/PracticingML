# PracticingML
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>AF_Created_Follow_Up_Action__c</fullName>
    <label>Created Follow Up Action ID</label>
    <type>Text</type>
    <length>18</length>
    <description>Stores the Task ID of the follow-up Task</description>
</CustomField>


<?xml version="1.0" encoding="UTF-8"?>
<CustomField xmlns="http://soap.sforce.com/2006/04/metadata">
    <fullName>AF_Type__c</fullName>
    <label>Type</label>
    <type>Picklist</type>
    <valueSet>
        <valueSetDefinition>
            <sorted>false</sorted>
            <value>
                <fullName>Task</fullName>
                <default>false</default>
            </value>
            <value>
                <fullName>Opportunity</fullName>
                <default>false</default>
            </value>
            <value>
                <fullName>Topic</fullName>
                <default>false</default>
            </value>
            <value>
                <fullName>Milestone</fullName>
                <default>false</default>
            </value>
        </valueSetDefinition>
    </valueSet>
</CustomField>
