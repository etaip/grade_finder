//
//  RestaurantTableViewController.swift
//  GradeFinder
//
//  Created by Etai Plushnick on 6/23/18.
//  Copyright © 2018 Etai Plushnick. All rights reserved.
//

import UIKit
import os.log

class RestaurantTableViewController: UITableViewController {
    //MARK: Properties
    
    var restaurants = [Restaurant]();
    var restaurantName: String?
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        sendGradeRequest()

        // Uncomment the following line to preserve selection between presentations
        // self.clearsSelectionOnViewWillAppear = false

        // Uncomment the following line to display an Edit button in the navigation bar for this view controller.
        // self.navigationItem.rightBarButtonItem = self.editButtonItem
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    // MARK: - Table view data source

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }

    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return restaurants.count
    }

    //MARK: Private Methods
    @IBAction func sendGradeRequest() {
        guard let restaurantName = restaurantName else {
            fatalError("restaurantName is nil!")
        }
        
        let url = URL(string: "https://zdf0mt0w6k.execute-api.us-east-1.amazonaws.com/dev/grade/\(restaurantName)")
        
        let task = URLSession.shared.dataTask(with: url!) { (data, response, error) in
            if let data = data {
                do {
                    let jsonSerialized = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                    if let json = jsonSerialized, let url = json["url"], let explanation = json["explanation"] {
                        os_log(url as! StaticString, log: OSLog.default, type: .info)
                        os_log(explanation as! StaticString, log: OSLog.default, type: .info)
                    }
                } catch let error as NSError {
                    os_log("Error - JSON serialization failed: %@", log: OSLog.default, type: .error, error)
                }
            } else if let error = error {
                os_log("Error - request failed: %@", log:OSLog.default, type: .error, error as CVarArg)
            }
        }
        
        task.resume()
    }
    
    /*
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "reuseIdentifier", for: indexPath)

        // Configure the cell...

        return cell
    }
    */

    /*
    // Override to support conditional editing of the table view.
    override func tableView(_ tableView: UITableView, canEditRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the specified item to be editable.
        return true
    }
    */

    /*
    // Override to support editing the table view.
    override func tableView(_ tableView: UITableView, commit editingStyle: UITableViewCellEditingStyle, forRowAt indexPath: IndexPath) {
        if editingStyle == .delete {
            // Delete the row from the data source
            tableView.deleteRows(at: [indexPath], with: .fade)
        } else if editingStyle == .insert {
            // Create a new instance of the appropriate class, insert it into the array, and add a new row to the table view
        }    
    }
    */

    /*
    // Override to support rearranging the table view.
    override func tableView(_ tableView: UITableView, moveRowAt fromIndexPath: IndexPath, to: IndexPath) {

    }
    */

    /*
    // Override to support conditional rearranging of the table view.
    override func tableView(_ tableView: UITableView, canMoveRowAt indexPath: IndexPath) -> Bool {
        // Return false if you do not want the item to be re-orderable.
        return true
    }
    */

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}
