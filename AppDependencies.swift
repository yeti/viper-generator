
//
//  AppDependencies.swift
//

import UIKit

class AppDependencies {
  
  
	  var homeWireframe = HomeWireframe()
  
	  var mapWireframe = MapWireframe()
  
  
  
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
    homePresenter.wireframe = homeWireFrame
    homeDataManager.interactor = homeInteractor
    //TODO: Set the DataMangaers DataStore

    // Instantiate wireframes
    homeWireframe.presenter = homePresenter
    homeWireframe.rootWireFrame = rootWire

    //TODO: Configure Home DataManager 
    
    // MARK: - Map Module
    let mapPresenter = MapPresenter()
    let mapInteractor = MapInteractor()
    let mapDataManager = MapDataManager()

    mapInteractor.presenter = mapPresenter
    mapInteractor.dataManager = mapDataManager
    mapPresenter.interactor = mapInteractor
    mapPresenter.wireframe = mapWireFrame
    mapDataManager.interactor = mapInteractor
    //TODO: Set the DataMangaers DataStore

    // Instantiate wireframes
    mapWireframe.presenter = mapPresenter
    mapWireframe.rootWireFrame = rootWire

    //TODO: Configure Map DataManager 
    
  }

}
