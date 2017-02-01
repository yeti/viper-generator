module = '''
package com.{{ lower_project_name }}.{{ lower_module_name }};

import android.content.Context;
import android.view.LayoutInflater;

import com.{{ lower_project_name }}.network.{{ upper_project_name }}NetworkService;

import javax.inject.Named;

import dagger.Module;
import dagger.Provides;

@Module
public class {{ upper_module_name }}Module {
    private final {{ upper_module_name }}Activity activity;

    public {{ upper_module_name }}Module({{ upper_module_name }}Activity activity) { this.activity = activity; }

    @Provides
    @Named("activity")
    Context provideActivityContext() {
        return activity;
    }

    @Provides
    {{ upper_module_name }}Presenter providePresenter({{ upper_module_name }}Interactor interactor) {
        return new {{ upper_module_name }}Presenter(activity, interactor);
    }

    @Provides
    {{ upper_module_name }}Interactor provideInteractor({{ upper_project_name }}NetworkService networkService) {
        return new {{ upper_module_name }}Interactor(networkService);
    }

    @Provides
    LayoutInflater provideLayoutInflater() {
        return activity.getLayoutInflater();
    }
}
'''


activity = '''
package com.{{ lower_project_name }}.{{ lower_module_name }};

import android.support.v7.app.AppCompatActivity;

public class {{ upper_module_name }}Activity extends AppCompatActivity {
    private {{ upper_module_name }}Component m{{ upper_module_name }}Component;

    // TODO: THIS IS INCOMPLETE
}
'''


component = '''
package com.{{ lower_project_name }}.{{ lower_module_name }};

import com.{{ lower_project_name }}.dependencies.ActivityScope;
import com.{{ lower_project_name }}.dependencies.ApplicationComponent;

import dagger.Component;

@ActivityScope
@Component(dependencies = {{ upper_module_name }}Component.class, modules = { {{ upper_module_name }}Module.class })
public interface {{ upper_module_name }}Component {
    void inject({{ upper_module_name }}Activity activity);
}
'''


interactor = '''
package com.{{ lower_project_name }}.{{ lower_module_name }};

import com.{{ lower_project_name }}.network.{{ upper_project_name }}NetworkService;

public class {{ upper_module_name }}Interactor {
    private {{ upper_project_name }}NetworkService mNetworkService;

    public {{ upper_module_name }}Interactor({{ upper_project_name }}NetworkService networkService) {
        mNetworkService = networkService;
    }

}
'''


presenter = '''
package com.{{ lower_project_name }}.{{ lower_module_name }};

import android.os.Bundle;

import com.{{ lower_project_name }}.BasePresenter;

import org.json.JSONObject;

public class {{ upper_module_name }}Presenter implements BasePresenter {
    private {{ upper_module_name }}Activity mActivity;
    private {{ upper_module_name }}Interactor mInteractor;

    public {{ upper_module_name }}Presenter(AssessmentActivity activity, {{ upper_module_name }}Interactor interactor) {
        mActivity = activity;
        mInteractor = interactor;
    }


    @Override
    public void onCreate(Bundle savedInstanceState) {

    }

    @Override
    public void onResume() {

    }

    @Override
    public void updateWithMachineInfo(JSONObject obj) {

    }
}
'''


fragment = '''
package com.{{ lower_project_name }}.{{ lower_module_name }};

import android.support.v4.app.Fragment;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.flexline.R;

public class {{ upper_fragment_name }}Fragment extends Fragment {
    private View view;

    private {{ upper_module_name }}Activity mActivity;
    private {{ upper_module_name }}Presenter mPresenter;

    public {{ upper_fragment_name }}Fragment() {}

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
    }

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater,
                             ViewGroup container,
                             Bundle savedInstanceState) {
        view = inflater.inflate(R.layout.fragment_login, container, false);

        mActivity = ({{ upper_module_name }}Activity) getActivity();
        mPresenter = mActivity.mPresenter;

        return view;
    }

    @Override
    public void onActivityCreated(Bundle savedInstanceState) {
        // Button listeners, etc

        super.onActivityCreated(savedInstanceState);
    }
}
'''


# TODO: xml templates
# Include note to move them out of directory and into the layouts directory after generation?
