
//
//  HomeWireframe.swift
//

import UIKit

class HomeWireframe: NSObject {
  var rootWireFrame : RootWireFrame?
  var presenter : HomePresenter?

  
  var homeListViewController : HomeListViewController?
  

  func homeStoryboard() -> UIStoryboard{
    let storyboard = UIStoryboard(name: "Home", bundle: NSBundle.mainBundle())
    return storyboard
  }

}
