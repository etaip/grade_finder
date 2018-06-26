//
//  Restaurant.swift
//  GradeFinder
//
//  Created by Etai Plushnick on 6/23/18.
//  Copyright © 2018 Etai Plushnick. All rights reserved.
//

import UIKit

class Restaurant {
    //MARK: Properties
    
    var name: String
    var grade: Grade
    var address: String
    
    //MARK: Initialization
    init(name: String, grade: Grade, address: String) {
        self.name = name
        self.grade = grade
        self.address = address
    }
}
