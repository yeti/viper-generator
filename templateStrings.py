viewControllerTemplate = '''
//
//  {{ view }}ViewController.swift
//
//

import UIKit

class {{ name.capitalize() }}ViewController: UIViewController{
  
  var presenter : {{ name }}Presenter?
  
  override func viewDidLoad() {
      super.viewDidLoad()
      // Do any additional setup after loading the view.
  }
  override func viewWillAppear(animated: Bool) {

  }

  override func didReceiveMemoryWarning() {
      super.didReceiveMemoryWarning()
      // Dispose of any resources that can be recreated.
  }

}
'''
presenterTemplate = '''
//
//  {{ name }}Presenter.swift
//
//

import UIKit

class {{ name }}Presenter: NSObject {
  
  var wireframe : {{ name }}Wireframe?
  {% for view in viewList%}
  var {{ view.lower() }}ViewController : {{ view }}ViewController?
  {% endfor %}
  var interactor : {{ name }}Interactor?

}
'''
interactorTemplate = '''
//
//  {{ name }}Interactor.swift
//

import UIKit

class {{ name.capitalize() }}Interactor: NSObject {
  
  var presenter : {{ name }}Presenter?
  var dataStore : {{ name }}DataStore?
  
}

'''

wireframeTemplate = '''
//
//  {{name}}Wireframe.swift
//

import UIKit

class {{ name.capitalize() }}Wireframe: NSObject {
  var rootWireFrame : RootWireFrame?
  var presenter : {{name}}Presenter?

  {% for view in viewList%}
  var {{ view.lower() }}ViewController : {{ view }}ViewController?
  {% endfor %}

  var mapWireFrame : {{name}}Wireframe?
  

}

'''

datamanagerTemplate = '''
//
//  {{ name }}DataManager.swift
//

import UIKit

class {{ name.capitalize() }}Interactor: NSObject {
  
  var presenter : {{ name }}Presenter?
  
}

'''

dependenciesTemplate = '''
//
//  AppDependencies.swift
//

import UIKit

class AppDependencies {
  
  {% for module in modules %}
	  var {{ module.name.lower() }}Wireframe = {{module.name.capitalize() }}Wireframe()
  {% endfor %}
  
  
  init() {
    configureDependencies()
  }
  
  /*
  func installViewControllersIntoWindow(window: UIWindow){
    // Initialize the root view controller
  }
  */
 
  func configureDependencies(){
    // set up relations to all wireframes
    //Root Wireframe
    let rootWire = RootWireFrame()

    //Data Store
    //TODO: Create DataStore

    {% for module in modules %}
    // MARK: - {{ module.name.capitalize() }} Module
    let {{ module.name.lower() }}Presenter = {{ module.name.capitalize() }}Presenter()
    let {{ module.name.lower() }}Interactor = {{ module.name.capitalize() }}Interactor()
    let {{ module.name.lower() }}DataManager = {{ module.name.capitalize() }}DataManager()

    {{ module.name.lower() }}Interactor.presenter = {{ module.name.lower() }}Presenter
    {{ module.name.lower() }}Interactor.dataManager = {{ module.name.lower() }}DataManager
    {{ module.name.lower() }}Presenter.interactor = {{ module.name.lower() }}Interactor
    {{ module.name.lower() }}Presenter.wireframe = {{ module.name.lower() }}WireFrame
    {{ module.name.lower() }}DataManager.interactor = {{ module.name.lower() }}Interactor
    //TODO: Set the DataMangaers DataStore

    // Instantiate wireframes
    {{ module.name.lower() }}Wireframe.presenter = {{ module.name.lower() }}Presenter
    {{ module.name.lower() }}Wireframe.rootWireFrame = rootWire

    //TODO: Configure {{ module.name.capitalize() }} DataManager 
    {% endfor %}
  }

}

'''
rootWireframe = '''
//
//  RootWireFrame.swift
//

import UIKit

class RootWireFrame: NSObject, UITabBarDelegate {
  
   // TODO: Add Initial View Controllers
}

'''











