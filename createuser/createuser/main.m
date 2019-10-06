//
//  main.m
//  createuser
//
//  Created by Greg Neagle on 8/13/19.
//
//  Copyright 2019 Greg Neagle.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.


#include <libgen.h> // for basename()

#import <Foundation/Foundation.h>
#import <OpenDirectory/OpenDirectory.h>


ODNode * localDSNode() {
    // returns local DS node
    ODSession * mySession = [ODSession defaultSession];
    if (mySession == nil) {
        return nil;
    }
    NSError * err = nil;
    ODNode *node = [ODNode nodeWithSession:mySession name:@"/Local/Default" error: &err];
    if (err != nil) {
        NSLog(@"Could not get local DS node: %@", err);
    }
    return node;
}

ODRecord * getUserRecord(NSString * userName) {
    // Returns a user record
    ODRecord * record = nil;
    NSError * err = nil;
    ODNode * node = localDSNode();
    if (node != nil) {
        record = [node recordWithRecordType:kODRecordTypeUsers name:userName attributes:nil error: &err];
        if (err != nil) {
            NSLog(@"Could not get user record for %@: %@", userName, err);
        }
    }
    return record;
}

ODRecord * createUserRecord(NSString * userName) {
    // Creates a user record and returns it
    ODRecord * record = nil;
    NSError * err = nil;
    ODNode * node = localDSNode();
    if (node != nil) {
        record = [node createRecordWithRecordType:kODRecordTypeUsers name:userName attributes:nil error: &err];
        if (err != nil) {
            NSLog(@"Could not create user record for %@: %@", userName, err);
        }
    }
    return record;
}

Boolean setAttributesForUser(NSDictionary * attrs, ODRecord * userRecord, NSArray * attrsToSkip) {
    // Sets attributes for user record
    if (attrsToSkip == nil) {
        attrsToSkip = @[];
    }
    NSError * err = nil;
    if (userRecord != nil) {
        for (NSString * key in attrs) {
            if (![attrsToSkip containsObject: key]){
                Boolean success = [userRecord setValue:attrs[key] forAttribute:key error: &err];
                if (!success) {
                    NSLog(@"Could not set attribute %@ to %@: %@", key, attrs[key], err);
                    return NO;
                }
            }
        }
        return YES;
    }
    return NO;
}

id readPlist(NSString * filename) {
    // returns data structure from a plist file
    // attempt to read the file
    NSData * plistData = [NSData dataWithContentsOfFile: filename];
    if (plistData == nil) {
        NSLog(@"Could not read data from %@!", filename);
        return nil;
    }
    // attempt to parse it as a plist
    NSPropertyListFormat fileFormat = 0;
    NSError * err = nil;
    id plist = [NSPropertyListSerialization propertyListWithData:plistData options:NSPropertyListImmutable format:&fileFormat error:&err];
    if (err != nil) {
        NSLog(@"Could not parse plist data from %@: %@", filename, err);
        return nil;
    }
    return plist;
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        if (argc != 2) {
            fprintf(stderr, "Error: %s takes exactly one argument: a path to an Open Directory user plist to import.\n", basename((char *)argv[0]));
            return -1;
        }
        // attempt to read in the passed-in file
        NSString * filename = [NSString stringWithCString:argv[1] encoding:NSUTF8StringEncoding];
        id userdata = readPlist(filename);
        if (userdata == nil) {
            return -1;
        }
        NSArray * usernameList = [(NSDictionary *)userdata objectForKey: @"name"];
        if (usernameList == nil) {
            NSLog(@"Could not get user name from plist - missing key 'name'");
            return -1;
        }
        NSString * username = usernameList[0];
        if (username == nil) {
            NSLog(@"Could not get user name from plist!");
            return -1;
        }
        NSArray * attrsToSkip = @[];
        ODRecord * record = getUserRecord(username);
        if (record == nil) {
            // create the record
            record = createUserRecord(username);
            if (record == nil) {
                NSLog(@"Failed to create user record for %@", username);
                return -1;
            }
        } else {
            // updating existing user record
            // in Mojave + we are not allowed to update the uid or home without user approval
            attrsToSkip = @[@"uid", @"home"];
        }
        Boolean success = setAttributesForUser((NSDictionary *)userdata, record, attrsToSkip);
        if (!success) {
            return -1;
        }
    }
    return 0;
}
