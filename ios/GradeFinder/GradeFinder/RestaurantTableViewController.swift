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
        
        restaurants.removeAll()
        sendGradeRequest()
        os_log("got here", log: OSLog.default, type: .debug)

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

    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cellIdentifier = "RestaurantTableViewCell"
        guard let cell = tableView.dequeueReusableCell(withIdentifier: cellIdentifier, for: indexPath) as? RestaurantTableViewCell else {
            fatalError("The dequeued cell is not an instance of RestaurantTableViewCell.")
        }
        
        let restaurant = restaurants[indexPath.row]
        cell.nameLabel.text = restaurant.name
        cell.addressLabel.text = restaurant.address
        cell.gradeImage.image = loadPhoto(grade: restaurant.grade)
        
        return cell
    }
    
    //MARK: Private Methods
    @IBAction func sendGradeRequest() {
        guard let restaurantName = restaurantName else {
            fatalError("restaurantName is nil!")
        }
        
        guard let restaurantNameEncoded = restaurantName.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) else {
            fatalError("Invalid encoding of restaurantName \(restaurantName)")
        }
        
        let url = URL(string: "https://zdf0mt0w6k.execute-api.us-east-1.amazonaws.com/dev/grade/\(restaurantNameEncoded)")
        let semaphore = DispatchSemaphore(value: 0)
        let task = URLSession.shared.dataTask(with: url!) { (data, response, error) in
            if let data = data {
                do {
                    let jsonSerialized = try JSONSerialization.jsonObject(with: data, options: []) as? [Any]
                    if let results = jsonSerialized as? [Dictionary<String, String>] {
                        os_log("JSON response is: %@", log: OSLog.default, type: .info, results)
                        for result in results {
                            guard let name = result["name"], let address = result["address"], let borough = result["borough"] else {
                                os_log("Missing fields in restaurant: %@", log: OSLog.default, type: .info, result)
                                semaphore.signal()
                                return
                            }
                            
                            var grade: String
                            if (result["grade"] != nil) && result["grade"] != "" {
                                grade = result["grade"]!
                            } else {
                                grade = "Not Yet Graded"
                            }
                            
                            let restaurant = Restaurant(name: name, grade: Grade(rawValue: grade)!, address: self.constructFullAddress(address: address, borough: borough))
                            self.restaurants.append(restaurant)
                        }
                    }
                } catch let error as NSError {
                    os_log("Error - JSON serialization failed: %@", log: OSLog.default, type: .error, error)
                }
            } else if let error = error {
                os_log("Error - request failed: %@", log:OSLog.default, type: .error, error as CVarArg)
            }
            semaphore.signal()
        }
        
        task.resume()
        _ = semaphore.wait(timeout: DispatchTime.distantFuture)
    }
    
    private func constructFullAddress(address: String, borough: String) -> String {
        return address + " " + borough + ", NY"
    }

    private func loadPhoto(grade: Grade) -> UIImage {
        switch (grade) {
        case .A:
            return UIImage(named: "gradeA")!
        case .B:
            return UIImage(named: "gradeB")!
        case .C:
            return UIImage(named: "gradeC")!
        case .GradePending:
            return UIImage(named: "gradePending")!
        case .NotYetGraded:
            return UIImage(named: "gradePending")!
        }
    }
    
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
