//
//  RestaurantTableViewCell.swift
//  GradeFinder
//
//  Created by Etai Plushnick on 6/23/18.
//  Copyright © 2018 Etai Plushnick. All rights reserved.
//

import UIKit

class RestaurantTableViewCell: UITableViewCell {
    //MARK: Properties
    @IBOutlet weak var gradeImage: UIImageView!
    @IBOutlet weak var nameLabel: UILabel!
    @IBOutlet weak var addressLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }

    override func setSelected(_ selected: Bool, animated: Bool) {
        super.setSelected(selected, animated: animated)

        // Configure the view for the selected state
    }

}
