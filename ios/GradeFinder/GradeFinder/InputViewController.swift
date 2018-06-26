//
//  InputViewController.swift
//  GradeFinder
//
//  Created by Etai Plushnick on 6/22/18.
//  Copyright © 2018 Etai Plushnick. All rights reserved.
//

import UIKit
import os.log

class InputViewController: UIViewController, UITextFieldDelegate {
    //MARK: Properties
    @IBOutlet weak var restaurantNameTextField: UITextField!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        // Do any additional setup after loading the view, typically from a nib.
        restaurantNameTextField.delegate = self
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    //MARK: UITextFieldDelegate
    func textFieldShouldReturn(_ textField: UITextField) -> Bool {
        // Hide the keyboard
        textField.resignFirstResponder()
        return true
    }
    
    //MARK: Navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        super.prepare(for: segue, sender: sender)
        
        guard let event = sender as? UITextField, event === restaurantNameTextField else {
            os_log("The text field did not send any input, cancelling", log: OSLog.default, type: .info)
            return
        }
        
        guard let destination = segue.destination as? RestaurantTableViewController else {
            fatalError("Invalid destination controller!")
        }
        
        destination.restaurantName = event.text
    }
}

