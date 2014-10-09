
//
//  AppDependencies.swift
//

import UIKit

class AppDependencies {
  
  
	  var homeWireframe = HomeWireframe()
  
	  var captureWireframe = CaptureWireframe()
  
  
  
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

    
    // MARK: - Home Module
    let homePresenter = HomePresenter()
    let homeInteractor = HomeInteractor()
    let homeDataManager = HomeDataManager()

    homeInteractor.presenter = homePresenter
    homeInteractor.dataManager = homeDataManager
    homePresenter.interactor = homeInteractor
    homePresenter.wireframe = homeWireframe
    homeDataManager.interactor = homeInteractor
    //TODO: Set the DataMangaers DataStore

    // Instantiate wireframes
    homeWireframe.presenter = homePresenter
    homeWireframe.rootWireFrame = rootWire

    //TODO: Configure Home DataManager 
    
    // MARK: - Capture Module
    let capturePresenter = CapturePresenter()
    let captureInteractor = CaptureInteractor()
    let captureDataManager = CaptureDataManager()

    captureInteractor.presenter = capturePresenter
    captureInteractor.dataManager = captureDataManager
    capturePresenter.interactor = captureInteractor
    capturePresenter.wireframe = captureWireframe
    captureDataManager.interactor = captureInteractor
    //TODO: Set the DataMangaers DataStore

    // Instantiate wireframes
    captureWireframe.presenter = capturePresenter
    captureWireframe.rootWireFrame = rootWire

    //TODO: Configure Capture DataManager 
    
  }

}
